# coding: utf-8

import os
import heapq


def top_huge_dirs_from_ncdu(topN, nodes, parent_path='', max_depth=3, depth=0):
    if isinstance(nodes, dict):
        size = nodes.get('dsize', 0)
        path = os.path.join(parent_path, nodes.get('name'))
        if depth > max_depth:
            return size
        return {path: size}

    node = nodes[0]
    subnodes = nodes[1:]
    path = os.path.join(parent_path, node.get('name'))

    if depth >= max_depth:
        ret = node.get('dsize', 0)
    else:
        ret = {}

    for subnode in subnodes:
        value = top_huge_dirs_from_ncdu(topN, subnode, path, max_depth, depth=depth + 1)
        if depth >= max_depth:
            ret += value
        else:
            ret.update(value)
            hugest_paths = heapq.nlargest(topN, ret, key=ret.get)
            ret = {p: ret.get(p) for p in hugest_paths}

    if depth == max_depth:
        return {path: ret}
    return ret


# not used now
def top_huge_files_from_ncdu(path='', blocks=[], res={}):
    dir_name = blocks[0].get('name')
    if dir_name.startswith('/'):
        path += dir_name
    else:
        path += '/' + dir_name

    for idx, block in enumerate(blocks):
        if isinstance(block, list):
            top_huge_files_from_ncdu(path, block, res)

        if isinstance(block, dict):
            if idx == 0:
                file_name = path
            else:
                file_name = path + '/' + block.get('name')
            # Directories in xfs do not have 'dsize' key. (?)
            size = block.get('dsize', 0)
            res[file_name] = size

    return res
