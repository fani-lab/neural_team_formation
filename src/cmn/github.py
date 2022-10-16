import pandas as pd
from tqdm import tqdm

from src.cmn.team import Team
from src.cmn.developer import Developer


class Repo(Team):

    def __init__(self, idx: int, contributors: list, name: str, languages_lines: list, nforks: int,
                 nstargazers: int, created_at: str, pushed_at: str, ncontributions: list, releases: list):

        super().__init__(id=idx, members=contributors, skills=None, datetime=created_at)
        self.name = name
        self.nforks = nforks
        self.nstargazers = nstargazers
        self.pushed_at = pushed_at
        self.ncontributions = ncontributions
        self.releases = releases
        self.languages_lines = languages_lines
        self.skills = self.set_skills()

    def set_skills(self):
        skills = set()
        for language in self.languages_lines: skills.add(language[0].lower())
        return skills

    @staticmethod
    def read_data(datapath, output, index, filter, settings):
        try:
            return super(Repo, Repo).load_data(output, index)
        except (FileNotFoundError, EOFError) as e:
            print(f"Pickles not found! Reading raw data from {datapath} ...")
            raw_dataset = pd.read_csv(datapath, converters={'collabs': eval, 'langs': eval, 'rels': eval})
            dict_of_teams = dict(); candidates = {}
            try:
                for idx, row in tqdm(raw_dataset.iterrows(), total=len(raw_dataset)):
                    contributors = row['collabs']
                    list_of_developers = list()
                    list_of_contributions = list()

                    for contributor in contributors:
                        if (idname := f"{contributor['id']}_{contributor['login']}") not in candidates:
                            candidates[idname] = Developer(name=contributor['login'], id=contributor['id'], url=contributor['url'])
                        list_of_developers.append(candidates[idname])
                        list_of_contributions.append(contributor['contributions'])

                    repo_name = row['repo']
                    languages_lines = list(row['langs'].items())
                    nstargazers = row['stargazers_count']
                    nforks = row['forks_count']
                    created_at = row['created_at']
                    pushed_at = row['pushed_at']
                    ncontributions = row['collabs']
                    releases = row['rels']

                    dict_of_teams[idx] = Repo(idx=idx, contributors=list_of_developers, name=repo_name, releases=releases,
                                              languages_lines=languages_lines, nstargazers=nstargazers,
                                              nforks=nforks, created_at=created_at, pushed_at=pushed_at, ncontributions=ncontributions)
            except Exception as e: raise e

            return super(Repo, Repo).read_data(dict_of_teams, output, filter, settings)
