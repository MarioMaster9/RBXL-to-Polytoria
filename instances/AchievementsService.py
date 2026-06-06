from .Instance import Instance
class AchievementsService(Instance):
    ClassName = "AchievementsService"
    Properties = [
        ["UseAchievementSound", "boolean"],
        ["NotifyAchievements", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(AchievementsService.Properties)
        self.Name = "Achievements"
        self.UseAchievementSound = True
        self.NotifyAchievements = True