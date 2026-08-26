function rpg:endless/member/clear_boons
tag @s remove rpg.end.member
tag @s remove rpg.end.member.current
scoreboard players set @s rpg_end_pick 0
scoreboard players set @s rpg_end_leave 0
scoreboard players set @s rpg_end_claim 1
scoreboard players set @s rpg_end_power 0
scoreboard players set @s rpg_end_vital 0
