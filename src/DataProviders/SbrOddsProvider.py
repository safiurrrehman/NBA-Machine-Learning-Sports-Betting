from sbrscrape import Scoreboard

class SbrOddsProvider:
    
    """ Abbreviations dictionary for team location which are sometimes saved with abbrev instead of full name. 
    Moneyline options name require always full name
    Returns:
        string: Full location name
    """    

    def __init__(self, sportsbook="fanduel"):
        self.sportsbook = sportsbook

    
    def get_odds(self):
        """Function returning odds from Sbr server's json content

        Returns:
            dictionary: [home_team_name + ':' + away_team_name: { home_team: money_line_odds, away_team: money_line_odds }, under_over_odds: val]
        """
        sb = Scoreboard(sport="NBA")
        games = sb.games if hasattr(sb, 'games') else []
        dict_res = {}
        for game in games:
            # Get team names
            home_team_name = self._get_team_name(game['home_team'])
            away_team_name = self._get_team_name(game['away_team'])
            

            # Get money line bet values
            money_line_home_value = self._get_money_line_value(game['home_ml'])
            money_line_away_value = self._get_money_line_value(game['away_ml'])
            
            # Get totals bet value
            totals_value = self._get_totals_value(game['total'])
            
            dict_res[home_team_name + ':' + away_team_name] = {
                'under_over_odds': totals_value,
                home_team_name: {'money_line_odds': money_line_home_value},
                away_team_name: {'money_line_odds': money_line_away_value}
            }

        return dict_res
    
    def _get_team_name(self, team_name):
        """Function to process team name and apply any necessary replacements"""
        team_name = team_name.replace("Los Angeles Clippers", "LA Clippers")
        return team_name

    def _get_money_line_value(self, ml_dict):
        """Function to get the money line value for the selected sportsbook"""
        if self.sportsbook in ml_dict:
            return ml_dict[self.sportsbook]
        return None

    def _get_totals_value(self, total_dict):
        """Function to get the totals value for the selected sportsbook"""
        if self.sportsbook in total_dict:
            return total_dict[self.sportsbook]
        return None