# 别西卜的化身：已有的别西卜模型，挂在一只弱化的卫道士上
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.tw.ev","rpg.te.av"],PersistenceRequired:1b,CustomName:{"text":"别西卜的化身","color":"#B5D957","bold":true,"italic":false},active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"minecraft:max_health",base:60},{id:"minecraft:attack_damage",base:5},{id:"minecraft:movement_speed",base:0.22}],Health:60f}
execute as @e[type=minecraft:vindicator,tag=rpg.te.av,distance=..1] at @s run function rpg:beelzebub/dress
execute as @e[type=minecraft:vindicator,tag=rpg.te.av,distance=..1] run function rpg:town/ev/g/avatar_hp
