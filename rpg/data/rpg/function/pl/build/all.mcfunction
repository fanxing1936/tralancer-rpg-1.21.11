# 失乐园打开：放好伊甸之门与四座河庭。旧档（#built 2 到 9）读进来时重放一遍
execute in rpg:paradise_lost unless loaded -30 80 -30 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded 39 80 39 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded -55 80 -175 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded -55 80 -65 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded 55 80 -175 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded 55 80 -65 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded 65 80 -55 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded 65 80 55 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded 175 80 -55 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded 175 80 55 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded -55 80 65 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded -55 80 175 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded 55 80 65 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded 55 80 175 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded -175 80 -55 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded -175 80 55 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded -65 80 -55 run return run schedule function rpg:pl/build/all 40t
execute in rpg:paradise_lost unless loaded -65 80 55 run return run schedule function rpg:pl/build/all 40t
scoreboard players set #built rpg_pl 10
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 0 run function rpg:pl/build/gate
scoreboard players set #c1 rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 -120 run function rpg:pl/build/court
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 -120 run function rpg:pl/build/court_1
execute in rpg:paradise_lost positioned 0 83 0 run kill @e[type=minecraft:marker,tag=rpg.pl.court1]
execute in rpg:paradise_lost positioned 0 83 0 run setblock 7 83 -103 minecraft:vault[ominous=false]{config:{loot_table:"rpg:loot/loot",override_loot_table_to_display:"rpg:vault/decoy",key_item:{id:"minecraft:trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}}}}
execute in rpg:paradise_lost positioned 0 83 0 run summon minecraft:marker 0 83 -120 {Tags:["rpg.pl.court","rpg.pl.court1"]}
scoreboard players set #c2 rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 positioned 120 82 0 run function rpg:pl/build/court
execute in rpg:paradise_lost positioned 0 83 0 positioned 120 82 0 run function rpg:pl/build/court_2
execute in rpg:paradise_lost positioned 0 83 0 run kill @e[type=minecraft:marker,tag=rpg.pl.court2]
execute in rpg:paradise_lost positioned 0 83 0 run setblock 127 83 17 minecraft:vault[ominous=false]{config:{loot_table:"rpg:loot/loot",override_loot_table_to_display:"rpg:vault/decoy",key_item:{id:"minecraft:trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}}}}
execute in rpg:paradise_lost positioned 0 83 0 run summon minecraft:marker 120 83 0 {Tags:["rpg.pl.court","rpg.pl.court2"]}
scoreboard players set #c3 rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 120 run function rpg:pl/build/court
execute in rpg:paradise_lost positioned 0 83 0 positioned 0 82 120 run function rpg:pl/build/court_3
execute in rpg:paradise_lost positioned 0 83 0 run kill @e[type=minecraft:marker,tag=rpg.pl.court3]
execute in rpg:paradise_lost positioned 0 83 0 run setblock 7 83 137 minecraft:vault[ominous=true]{config:{loot_table:"rpg:loot/loot_ominous",override_loot_table_to_display:"rpg:vault/decoy",key_item:{id:"minecraft:ominous_trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"灾厄试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}}}}
execute in rpg:paradise_lost positioned 0 83 0 run summon minecraft:marker 0 83 120 {Tags:["rpg.pl.court","rpg.pl.court3"]}
scoreboard players set #c4 rpg_pl 0
execute in rpg:paradise_lost positioned 0 83 0 positioned -120 82 0 run function rpg:pl/build/court
execute in rpg:paradise_lost positioned 0 83 0 positioned -120 82 0 run function rpg:pl/build/court_4
execute in rpg:paradise_lost positioned 0 83 0 run kill @e[type=minecraft:marker,tag=rpg.pl.court4]
execute in rpg:paradise_lost positioned 0 83 0 run setblock -113 83 17 minecraft:vault[ominous=true]{config:{loot_table:"rpg:loot/loot_ominous",override_loot_table_to_display:"rpg:vault/decoy",key_item:{id:"minecraft:ominous_trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"灾厄试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}}}}
execute in rpg:paradise_lost positioned 0 83 0 run summon minecraft:marker -120 83 0 {Tags:["rpg.pl.court","rpg.pl.court4"]}
scoreboard players set #sites rpg_pl 1
schedule function rpg:pl/build/sweep 10t
