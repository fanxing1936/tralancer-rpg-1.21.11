execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run particle minecraft:flash{color:16774876} ~ ~2 ~ 0 0 0 0 1 force
execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run particle minecraft:totem_of_undying ~ ~2 ~ 2 2 2 0.4 120 force
execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run particle minecraft:end_rod ~ ~6 ~ 3 4 3 0.02 80 force
execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run playsound minecraft:block.bell.resonate hostile @a[distance=..48] ~ ~ ~ 1 0.8
execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run tellraw @a[distance=..48] ["",{"text":"〖撒母耳记上 17:45〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"你来攻击我，是靠着刀枪和铜戟；我来攻击你，是靠着万军之耶和华的名。","color":"#E6DFCF","bold":false,"italic":false}]
# 圣殿誓约：战场里每个还没有的人各得一件，之后可以召友军雅克（add_jacques_ally.py）
execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run function rpg:jacques_ally/reward
# 装备养成：不屈之源与符石
execute at @e[type=minecraft:marker,tag=rpg.jqb.center,limit=1] run loot spawn ~ ~1 ~ loot rpg:forge/boss/resolve
function rpg:jacques_boss/clear
