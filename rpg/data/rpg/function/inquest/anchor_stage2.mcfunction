execute unless entity @s[tag=rpg.rite.medium] if score @s rpg_dm_lord matches 1 run return run function rpg:inquest/scan/1
execute unless entity @s[tag=rpg.rite.medium] if score @s rpg_dm_lord matches 2 run return run function rpg:inquest/scan/2
execute unless entity @s[tag=rpg.rite.medium] if score @s rpg_dm_lord matches 3 run return run function rpg:inquest/scan/3
execute unless entity @s[tag=rpg.rite.medium] if score @s rpg_dm_lord matches 4 run return run function rpg:inquest/scan/4
execute unless entity @s[tag=rpg.rite.medium] if score @s rpg_dm_lord matches 5 run return run function rpg:inquest/scan/5
execute unless entity @s[tag=rpg.rite.medium] if score @s rpg_dm_lord matches 6 run return run function rpg:inquest/scan/6
execute unless entity @s[tag=rpg.rite.medium] if score @s rpg_dm_lord matches 7 run return run function rpg:inquest/scan/7
execute if score @s rpg_totem matches 2300 run tellraw @a[distance=..18,gamemode=!spectator] ["",{"text":"[镇魔二阶段] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"攻击恶魔与右键布置仪式器物可提高稳定度；技能和挣脱会令其下降。","color":"gray","italic":false}]
tag @s remove rpg.rite.anchor.active
