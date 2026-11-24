# 失乐园打开：放好伊甸之门与四座河庭。旧档（#built 2 到 8）读进来时重放一遍
scoreboard players set #built rpg_pl 9
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 0 run function rpg:pl/build/gate
scoreboard players set #c1 rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 -120 run function rpg:pl/build/court
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 -120 run function rpg:pl/build/court_1
execute in rpg:paradise_lost positioned 0 83 0 run kill @e[type=minecraft:marker,tag=rpg.pl.court1]
execute in rpg:paradise_lost positioned 0 83 0 run setblock 7 83 -103 minecraft:vault[ominous=false]{config:{loot_table:"rpg:loot/loot",key_item:{id:"minecraft:trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}}}}
execute in rpg:paradise_lost positioned 0 83 0 run summon minecraft:marker 0 83 -120 {Tags:["rpg.pl.court","rpg.pl.court1"]}
scoreboard players set #c2 rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 positioned 120 82 0 run function rpg:pl/build/court
execute in rpg:paradise_lost positioned 0 83 0 positioned 120 82 0 run function rpg:pl/build/court_2
execute in rpg:paradise_lost positioned 0 83 0 run kill @e[type=minecraft:marker,tag=rpg.pl.court2]
execute in rpg:paradise_lost positioned 0 83 0 run setblock 127 83 17 minecraft:vault[ominous=false]{config:{loot_table:"rpg:loot/loot",key_item:{id:"minecraft:trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}}}}
execute in rpg:paradise_lost positioned 0 83 0 run summon minecraft:marker 120 83 0 {Tags:["rpg.pl.court","rpg.pl.court2"]}
scoreboard players set #c3 rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 120 run function rpg:pl/build/court
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 120 run function rpg:pl/build/court_3
execute in rpg:paradise_lost positioned 0 83 0 run kill @e[type=minecraft:marker,tag=rpg.pl.court3]
execute in rpg:paradise_lost positioned 0 83 0 run setblock 7 83 137 minecraft:vault[ominous=true]{config:{loot_table:"rpg:loot/loot_ominous",key_item:{id:"minecraft:ominous_trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"灾厄试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}}}}
execute in rpg:paradise_lost positioned 0 83 0 run summon minecraft:marker 0 83 120 {Tags:["rpg.pl.court","rpg.pl.court3"]}
scoreboard players set #c4 rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 positioned -120 82 0 run function rpg:pl/build/court
execute in rpg:paradise_lost positioned 0 83 0 positioned -120 82 0 run function rpg:pl/build/court_4
execute in rpg:paradise_lost positioned 0 83 0 run kill @e[type=minecraft:marker,tag=rpg.pl.court4]
execute in rpg:paradise_lost positioned 0 83 0 run setblock -113 83 17 minecraft:vault[ominous=true]{config:{loot_table:"rpg:loot/loot_ominous",key_item:{id:"minecraft:ominous_trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"灾厄试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}}}}
execute in rpg:paradise_lost positioned 0 83 0 run summon minecraft:marker -120 83 0 {Tags:["rpg.pl.court","rpg.pl.court4"]}
scoreboard players set #sites rpg_pl 1
execute in rpg:paradise_lost positioned 0 83 0 run forceload remove all
execute as @a[tag=rpg.pl.wait] run function rpg:pl/go
