from pathlib import Path

from pydantic import BaseModel

from .interface import ReadableRepoInterface


class Project(BaseModel):
    description: str
    tag: str


class ProjectsRepo(ReadableRepoInterface):
    def __init__(self, path: Path):
        files_list = list(path.glob("*.txt"))

        self.repo = {}

        for file in files_list:
            tag = file.name.split("_")[0]
            self.repo[tag] = []

            with open(file, "r") as f:
                descriptions = f.read().split("---")
            
            for description in descriptions:
                self.repo[tag].append(Project(description=description.strip(), tag=tag))

    def get_all(self):
        all_projects = [project for projects in self.repo.values() for project in projects]

        return all_projects
    
    def filter(self, **kwargs):
        tag = kwargs.get("tag", "")
        return self.repo.get(tag, [])
