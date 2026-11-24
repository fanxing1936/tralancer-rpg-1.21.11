# 6 行原本各自扫一遍全实体表找 @e[type=minecraft:item,tag=rpg.i.loot_trigger2]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run playsound minecraft:block.beacon.power_select player @a[distance=..7]
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run summon firework_rocket ~ ~-0.2 ~ {Life:0,LifeTime:0,FireworksItem:{id:firework_rocket,components:{fireworks:{flight_duration:0,explosions:[{shape:burst,has_twinkle:1b,has_trail:1b,colors:[I;16351261,16347951,16383998]}]}}}}
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run setblock ~ ~-1 ~ air
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run setblock ~ ~-1 ~ minecraft:vault[ominous=false]{config:{loot_table:"rpg:loot/loot",key_item:{id:"minecraft:trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}}}}
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run kill
