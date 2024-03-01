

	
import pydriller
import json


def _getMethodBody(method, source_code, file):
    """
    Given a method, it returns the body of the method.
    :param method: the method
    :param source_code: the source code
    :param file: the file
    :return: the body of the method
    """
    if method and source_code:
        lines = source_code.split("\n")
        start = method.start_line
        end = method.end_line
        method_body = "\n".join(lines[start - 1 : end])
        return method_body
    return None


i = 0
repourl ='https://github.com/shosetsuorg/shosetsu'
Commit = pydriller.Repository(path_to_repo=repourl).traverse_commits()
print(Commit)
commit = None
for c in Commit:

  commit = c
  i += 1
  if i == 69:
    break
print(commit)
# print(commit.modified_files[0])
modified_files = []
for m in commit.modified_files:
  modified_files.append(m)
i = i + 1
print(i)
for file in modified_files:
    # print(file._c_diff)
    print("FIleName", file.filename)
    print("\n\n\n\n")
    print(i)
    print("File DIff", file.diff)
    print("\n\n\n\n")
    for method in file.changed_methods:
        method_before = next((x for x in file.methods_before if x == method), None)
        print(method_before)
        print("\n\n\n\n")
        method_after = next((x for x in file.methods if x == method), None)
        print(method_after)
        print("\n\n\n\n")
        body_before = _getMethodBody(method_before, file.source_code_before, file)
        body_after = _getMethodBody(method_after, file.source_code, file)
        print(
            "MethodName",
            method.name,
            "\n\n\n\n\n\n\nBodyBefore",
            body_before,
            "\n\n\n\n\n\n",
            body_after,
        )
        print("\n\n\n\n")
    break
