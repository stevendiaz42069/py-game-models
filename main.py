import init_django_orm  # noqa: F401

import json

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as f_in:
        player_profile = json.load(f_in)
    if isinstance(player_profile, dict):
        player_list = player_profile.items()
    elif isinstance(player_profile, list):
        player_list = ((item["nickname"], item) for item in player_profile)
    else:
        raise ValueError("players.json must contain a list or dict of players")
    for nickname, player_data in player_list:
        race, created = Race.objects.get_or_create(
            name=player_data["race"]["name"],
            defaults={"description": player_data["race"]["description"]})
        for player_skill in player_data["race"].get("skills", []):
            skill, created = Skill.objects.get_or_create(
                name=player_skill["name"],
                race=race,
                defaults={"bonus": player_skill.get("bonus")})
        guild = None
        if player_data.get("guild"):
            guild, created = Guild.objects.get_or_create(
                name=player_data["guild"]["name"],
                defaults={
                    "description": player_data["guild"]["description"]})
        player, created = Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player_data["email"], "bio": player_data["bio"],
                "race": race,
                "guild": guild})


if __name__ == "__main__":
    main()
