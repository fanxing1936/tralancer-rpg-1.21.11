# 反向的仪式：逆着画的圈、黑烛、一半的血 → 罪仆现身，递出契约
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sin_shard"}] 3
execute store result score #h rpg_dm run data get entity @s Health
scoreboard players operation #h rpg_dm /= #2 rpg_tw
execute store result storage rpg:town dm.h int 1 run scoreboard players get #h rpg_dm
function rpg:town/demon/bleed with storage rpg:town dm
execute as @e[type=minecraft:interaction,tag=rpg.tnpc.altar,distance=..8,limit=1,sort=nearest] at @s run function rpg:town/demon/circle
tellraw @s ["",{"text":"〖","color":"#A276BE","bold":true,"italic":false},{"text":"罪仆","color":"#A276BE","bold":true,"italic":false},{"text":"〗","color":"#A276BE","bold":true,"italic":false},{"text":" 𝔖𝔦𝔫-𝔰𝔢𝔯𝔳𝔞𝔫𝔱","color":"#8F7430","italic":false},{"text":"  是谁逆着画了圈，点了黑烛……啊，是你。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Who drew the circle backwards and lit the black candle... ah. It's you.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.sv01 voice @s ~ ~ ~ 1 1
scoreboard players add #sid rpg_say 1
scoreboard players operation @s rpg_say = #sid rpg_say
execute store result score #due rpg_say run time query gametime
scoreboard players add #due rpg_say 115
function rpg:town/say/push {f:3}
execute store result score #due rpg_say run time query gametime
scoreboard players add #due rpg_say 214
function rpg:town/say/push {f:2}
execute store result score #due rpg_say run time query gametime
scoreboard players add #due rpg_say 327
function rpg:town/say/push {f:1}
scoreboard players enable @s rpg_dm_do
dialog show @s {"type":"minecraft:multi_action","title":["",{"text":"契约 · ","color":"#A276BE","bold":true,"italic":false},{"text":"投诚契约","color":"#E6DFCF","bold":true,"italic":false},{"text":" 𝔓𝔞𝔠𝔱 𝔬𝔣 𝔄𝔩𝔩𝔢𝔤𝔦𝔞𝔫𝔠𝔢","color":"#8F7430","bold":false,"italic":false}],"body":[{"type":"minecraft:plain_message","width":300,"contents":["",{"text":"立约人投入七十二柱一方，与教廷为敌。\n\n","color":"#E6DFCF","bold":false,"italic":false},{"text":"代价：魔化 +30；名字前多一枚魔印；圣水从此会烫伤你；在圣卫面前亮出罪器就会被通缉。\n","color":"#9C9A94","bold":false,"italic":false},{"text":"回头的路是有的（堕落者凭新约回头），但代价很高。","color":"#797979","bold":false,"italic":false}]}],"actions":[{"label":{"text":"签下","color":"#A276BE","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_dm_do set 11"}},{"label":{"text":"不签","color":"#E6DFCF","bold":true,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_dm_do set 12"}}],"columns":2,"can_close_with_escape":false,"pause":false,"after_action":"close"}
