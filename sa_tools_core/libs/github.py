import requests
import base64
import json
import logging
import datetime
from pathlib import Path, PurePath

from sa_tools_core.consts import GITHUB_API_ENTRYPOINT
from sa_tools_core.utils import get_config

logger = logging.getLogger(__name__)


def github_secret_func():
    return get_config('github')


class GithubRepo:
    def __init__(self, org, repo, entrypoint=None,
                 user_name=None, personal_token=None, secret_func=None,
                 author=None, skip_ssl=False):
        self.org = org
        self.repo = repo
        self.author = author
        self.entrypoint = entrypoint
        self.base_commit = None
        self.base_tree = None
        self.head_commit = None
        self.head_tree = None
        self.secret_func = secret_func
        self.session = requests.Session()
        if user_name and personal_token:
            self.user_name = user_name
            self.personal_token = personal_token
        else:
            (self.user_name, self.personal_token) = self.get_user_token_pair()
        self.session.auth = (self.user_name, self.personal_token)
        self.skip_ssl = skip_ssl

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.session:
            self.session.close()

    def get_user_token_pair(self):
        if self.secret_func:
            secret = self.secret_func()
            divided_secret = secret.split(':', 1)
            if len(divided_secret) != 2:
                raise ValueError("Invalid secret, suppose to be able to be split into 2 strings")
            return divided_secret
        raise ValueError("Please define either username & token or secret_func.")

    def make_request(self, method, api_path, **kwargs):
        r = self.session.request(method, f"{self.entrypoint}{api_path}", verify=(not self.skip_ssl), **kwargs)
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(r.text)
            raise e
        if r.status_code == 204:
            return None
        return r.json()

    def get_file(self, path, reference=None):
        """get content
        GET /repos/:owner/:repo/contents/:path
        :: params
        reference: str branch, tag or commit id, default: default branch of repo
        path: str relative path
        :: return
        dict
        """
        try:
            return self.make_request('GET', f"/repos/{self.org}/{self.repo}/contents/{path}",
                                 params={'ref': reference or 'master'})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise e

    def get_reference(self, reference):
        return self.make_request('GET', f"/repos/{self.org}/{self.repo}/git/ref/heads/{reference}")

    def get_commit(self, commit_sha):
        return self.make_request('GET', f"/repos/{self.org}/{self.repo}/git/commits/{commit_sha}")

    def update_a_file(self, path, content, message, sha=None):
        return self.make_request('PUT', f"/repos/{self.org}/{self.repo}/contents/{path}",
                                 data=json.dumps({
                                     'message': message,
                                     'content': base64.b64encode(content).decode(),
                                     'sha': sha
                                 }))

    def upload_one_file(self, content):
        """
        POST /repos/:owner/:repo/git/blobs
        :: input
        {
            "content": "Content of the blob",
            "encoding": "utf-8"
        }
        :: return
        {
            "url": "https://api.github.com/repos/octocat/example/git/blobs/3a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15",
            "sha": "3a0f86fb8db8eea7ccbb9a95f325ddbedfb25e15"
        }

        """
        return self.make_request('POST', f"/repos/{self.org}/{self.repo}/git/blobs",
                                 data=json.dumps({
                                     'content': base64.b64encode(content).decode(),
                                     'encoding': 'base64'
                                 }))

    def create_tree(self, base_tree, files):
        """ equivalent to  git add
        """
        return self.make_request('POST', f"/repos/{self.org}/{self.repo}/git/trees",
                                 data=json.dumps({
                                     'base_tree': base_tree,
                                     'tree': files
                                 }))

    def create_commit(self, base, tree, message):
        """ equivalent to git commit
        """
        return self.make_request('POST', f"/repos/{self.org}/{self.repo}/git/commits",
                                 data=json.dumps({
                                     'message': message,
                                     'tree': tree,
                                     'parents': [base]
                                 }))

    def create_reference(self, reference, commit_sha):
        return self.make_request('POST', f"/repos/{self.org}/{self.repo}/git/refs",
                                 data=json.dumps({
                                     'ref': f"refs/heads/{reference}",
                                     'sha': commit_sha
                                 }))

    def update_reference(self, reference, commit_sha):
        """ equivalent to git push
        PATCH /repos/:owner/:repo/git/refs/:ref
        """
        return self.make_request('PATCH', f"/repos/{self.org}/{self.repo}/git/refs/heads/{reference}",
                                 data=json.dumps({
                                     "sha": commit_sha,
                                     'force': False
                                 }))

    def create_pull_request(self, title, head, base, body='', maintainer_can_modify=True, draft=False, ):
        return self.make_request('POST', f"/repos/{self.org}/{self.repo}/pulls",
                                 data=json.dumps({
                                     'title': title,
                                     'head': head,
                                     'base': base,
                                     'body': body,
                                     'maintainer_can_modify': maintainer_can_modify,
                                     'draft': draft
                                 }))

    def merge_pull_request(self, pull_number, merge_method='merge'):
        """merge method: `rebase`, `squash`, `merge`"""
        return self.make_request('PUT', f"/repos/{self.org}/{self.repo}/pulls/{pull_number}/merge",
                                 data=json.dumps({
                                     'merge_method': merge_method
                                 }))

    def has_collaborator(self, username):
        """if present, return True, if not, return False"""
        r = self.session.request("GET", f"{self.entrypoint}/repos/{self.org}/{self.repo}/collaborators/{username}",
                                 verify=(not self.skip_ssl))
        if r.status_code == 204:
            return True
        elif r.status_code == 404:
            return False
        else:
            r.raise_for_status()

    def add_collaborator(self, username, permission=None):
        """permissions: `pull`, `push`, `admin`, `maintain`, `triage` 
        return None on default, raise exception if anything wrong
        """
        if permission is None:
            permission = 'push'
        self.make_request('PUT', f"/repos/{self.org}/{self.repo}/collaborators/{username}",
                                 data=json.dumps({
                                     'permission': permission
                                 }))

    def remove_collaborator(self, username):
        self.make_request('DELETE', f"/repos/{self.org}/{self.repo}/collaborators/{username}")

    def create_commit_comment(self, commit_sha, comment_content, path=None, position=None):
        comment = {'body': comment_content}
        if path:
            comment['path'] = path
        if position:
            comment['position'] = position
        return self.make_request('POST', f"/repos/{self.org}/{self.repo}/commits/{commit_sha}/comments",
                                 data=json.dumps(comment))

    def list_commit_comments(self, commit_sha):
        return self.make_request('GET', f"/repos/{self.org}/{self.repo}/commits/{commit_sha}/comments")

    # high level api starts here
    def add(self, files, base_reference):
        """add files to the tree, generate a tree , store the tree_sha to self.head_tree"""
        files_sha = []
        # upload
        for path, content in files.items():
            base_file = self.get_file(path, reference=base_reference)
            if base_file and base64.b64decode(base_file['content'].encode()) == content:
                logger.info(f'{path} unchange, ignored')
                continue
            upload_result = self.upload_one_file(content)
            files_sha += [{
                'path': path,
                'sha': upload_result['sha'],
                'type': 'blob',
                'mode': '100644'
            }]
        if len(files_sha) == 0:
            logger.info("changelist empty, ignored")
            return

        # add to index, need tree base sha
        base_branch = self.get_reference(base_reference)
        self.base_commit = self.get_commit(base_branch['object']['sha'])
        self.head_tree = self.create_tree(self.base_commit['tree']['sha'], files_sha)
        return self.head_tree

    def commit(self, message):
        self.head_commit = self.create_commit(self.base_commit['sha'], self.head_tree['sha'], message)
        logger.info('commit create: %s', self.head_commit['url'])

    def push(self, reference):
        try:
            self.update_reference(reference, self.head_commit['sha'])
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422:
                # error 422 , reference not exist, create reference
                self.create_reference(reference, self.head_commit['sha'])
            else:
                raise e

    def download(self, remote_path, local_path, reference='master'):
        """download a folder recursively, only file and directory supported, """
        file_or_dir = self.get_file(remote_path)
        if isinstance(file_or_dir, dict):
            # file, submodule, link, only file is supported now
            if file_or_dir['type'] != 'file':
                logger.warning('Only file and directory are supported, submodule and symlink are ignored.')
                logger.warning(f"{file_or_dir['type']} ignored : {file_or_dir['path']}")
                return
            with open(local_path, 'wb') as fp:
                fp.write(base64.b64decode(
                    file_or_dir['content'].encode()))
        else:
            # dir
            Path(local_path).mkdir(parents=True, exist_ok=True)
            for f in file_or_dir:
                self.download(f['path'], PurePath(local_path).joinpath(f['name']), reference=reference)

    def update_files(self, reference, files, message):
        """update reference
        reference: str branch, tag
        files: dict {file_path, filecontent}
            file_path -> str
            filecontent -> bytes
            example: {'example.md', b'Hello world', 'libs/example2.md', b'Hello world2'}
        possible error:
        Web failed, timeout, 404, 403.
        None fast forward.
        No change.
        """
        if len(files.keys()) == 1:
            # simple update file
            path = list(files.keys())[0]
            content = files[path]
            base_file = self.get_file(path, reference=reference)
            if not base_file:
                self.update_a_file(path, content, message)
            elif base64.b64decode(base_file['content'].encode()) == content:
                logger.info(f'{path} unchange, ignored')
            else:
                self.update_a_file(path, content, message, sha=base_file['sha'])
            return

        add_result = self.add(files, reference)
        if add_result:
            # do not continue if add not successful
            self.commit(message)
            self.push(reference)

    def submit_pr(self, base_branch, files, title,
                  body='', commit_message='', new_branch_name='',
                  auto_merge=False, merge_method='merge'):
        if not commit_message:
            commit_message = "Update {}".format(', '.join(files.keys()))
        if not new_branch_name:
            new_branch_name = "patch-{}".format(datetime.datetime.now().strftime('%m-%d.%H.%M'))
        add_result = self.add(files, base_branch)
        if not add_result:
            logger.info('Empty changelist, ignored')
            return
        # do not continue if add not successful
        self.commit(commit_message)
        self.push(new_branch_name)
        created_pr = self.create_pull_request(title, new_branch_name, base_branch, body=body)
        logger.info(f"PR create, url: {created_pr['html_url']}")
        if auto_merge:
            self.merge_pull_request(created_pr['number'], merge_method=merge_method)
            logger.info('PR was successfully merged')
        return created_pr
    
    def ensure_collaborator(self, username, permission=None):
        """permissions: `pull`, `push`, `admin`, `maintain`, `triage` 
        return None on default, raise exception if anything wrong
        """
        if self.has_collaborator(username):
            self.remove_collaborator(username)
        self.add_collaborator(username, permission=permission)


def commit_github(org, repo, branch, files, message, retry=2):
    """update files of a repo on a branch head.
    ::params:
        org: str
        repo: str
        branch: str
        files: dict {file_path, filecontent}
            file_path -> str
            filecontent -> bytes
            example: {'example.md', b'Hello world', 'libs/example2.md', b'Hello world2'}
    """
    return_value = -1
    with GithubRepo(org, repo, entrypoint=GITHUB_API_ENTRYPOINT, secret_func=github_secret_func) as gh:
        for _ in range(retry + 1):
            try:
                gh.update_files(branch, files, message)
                return_value = 0
                break
            except Exception as e:
                logger.warning(e)
                logger.warning('Request failed , retrying')
    return return_value


def submit_pr(org, repo, *args, **kwargs):
    with GithubRepo(org, repo, entrypoint=GITHUB_API_ENTRYPOINT, secret_func=github_secret_func) as gh:
        return gh.submit_pr(*args, **kwargs)
