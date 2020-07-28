import argparse

from sa_tools_core.libs.github import GithubRepo, GITHUB_API_ENTRYPOINT, github_secret_func
# ...

def operate_collaborator(args):
    repo = GithubRepo(args.org, args.repo, entrypoint=GITHUB_API_ENTRYPOINT, secret_func=github_secret_func)
    if args.action == 'add':
        repo.ensure_collaborator(args.username, permission=args.permission)
    if args.action == 'remove':
        repo.remove_collaborator(args.username)

def main():
    parser = argparse.ArgumentParser(
        description="operator github or ghe using cli"
    )

    subparsers = parser.add_subparsers(help='Sub commands', dest='subparser')
    subparsers.required = True

    collaborator = subparsers.add_parser('collaborator')


    collaborator.add_argument(
        "--org",
        help="github organization",
        required=True
    )
    collaborator.add_argument(
        "--repo",
        help="github repo name",
        required=True
    )
    collaborator.add_argument(
        "action",
        choices=["add", "remove"],
        help="action you want to take, add or remove a collaborator"
    )
    collaborator.add_argument(
        "--username",
        required=True,
        help="github username"
    )
    collaborator.add_argument(
        "--permission",
        default="push",
        choices=["pull", "push", "admin", "maintain", "triage"]
    )

    collaborator.set_defaults(func=operate_collaborator)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()