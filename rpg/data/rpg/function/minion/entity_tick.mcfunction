execute if entity @s[scores={rpg_mn_cd=1..}] run scoreboard players remove @s rpg_mn_cd 10
execute unless entity @a[distance=..12,gamemode=!spectator,gamemode=!creative,limit=1] run return 0
execute if entity @s[scores={rpg_mn_cd=..0}] run function rpg:minion/ability_dispatch
