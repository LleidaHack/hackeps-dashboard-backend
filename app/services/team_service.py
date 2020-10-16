
class TeamService():

    def __init__(self, db):
        self.firestore = db

    def get_all_teams(self, users):
        teams = self.firestore.collection(u'hackeps-2020').document(u'prod').collection(u'teams').get()
        team_list = list()
        
        for team in teams:
            team = team.to_dict()
            prov_members = list()
            for member in team['members']:
                if member is not None:
                    rmv_index = -1
                    for index, user in enumerate(users):
                        if user['uid'] == member.id:
                            rmv_index = index
                            prov_members.append(user)
                            break
                    if rmv_index != -1:
                        users.pop(rmv_index)
                            
            prov_team = {
                'name': team['name'], 
                'uid': team['uid'],
                'members': prov_members}
            team_list.append(prov_team)
        return team_list