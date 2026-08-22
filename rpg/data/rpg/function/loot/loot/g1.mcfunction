# 6 行原本各自扫一遍全实体表找 @e[type=minecraft:item,tag=rpg.i.loot_trigger2]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run playsound minecraft:block.beacon.power_select player @a[distance=..7]
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run summon firework_rocket ~ ~-0.2 ~ {Life:0,LifeTime:0,FireworksItem:{id:firework_rocket,components:{fireworks:{flight_duration:0,explosions:[{shape:burst,has_twinkle:1b,has_trail:1b,colors:[I;16351261,16347951,16383998]}]}}}}
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run setblock ~ ~-1 ~ air
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run setblock ~ ~-1 ~ minecraft:vault[ominous=false]{config:{loot_table:"rpg:loot/loot",key_item:{components:{"minecraft:lore":[{"extra":[{"color":"white","italic":false,"text":"+------------------+"}],"text":""},{"extra":[{"color":"white","italic":false,"text":"开辟神启的"},{"bold":true,"color":"gold","italic":false,"text":"[钥匙]"}],"text":""},{"extra":[{"color":"white","italic":false,"text":"唤出传奇的"},{"bold":true,"color":"gold","italic":false,"text":"[宝具]"}],"text":""},{"extra":[{"color":"white","italic":false,"text":"+------------------+"}],"text":""}],"minecraft:custom_name":{"extra":[{"bold":true,"color":"gold","italic":false,"text":"[legend]"},{"italic":false,"text":"试炼之匙"}],"text":""}},count:1,id:"minecraft:trial_key"}}}
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s run kill
