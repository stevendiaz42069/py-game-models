import init_django_orm  # noqa: F401

import json

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("py-game-models/players.json", "r") as f_in:
        player_profile = json.load(f_in)
        if isinstance(player_profile, dict):
            player_list = list(player_profile.items())
        for nickname, player_data in player_list:
            race, created = Race.objects.get_or_create(
                name=player_data["race"]["name"],
                defaults={"description": player_data["race"]["description"]})
            for player_skill in player_data["race"].get("skills", []):
                skill, created = Skill.objects.get_or_create(
                    name=player_skill["name"],
                    race=race,
                    defaults={"bonus": player_skill.get("bonus")})
            if player_data["guild"]:
                guild, created = Guild.objects.get_or_create(
                    name=player_data["guild"]["name"],
                    defaults={
                        "description": player_data["guild"]["description"]})
            player, created = Player.objects.get_or_create(
                nickname=nickname,
                race=race,
                guild=guild,
                defaults={
                    "email": player_data["email"], "bio": player_data["bio"]})


if __name__ == "__main__":
    main()
