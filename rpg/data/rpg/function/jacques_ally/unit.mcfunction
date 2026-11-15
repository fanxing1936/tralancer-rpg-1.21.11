# 友军雅克每刻（as/at 他）。
execute if entity @s[tag=rpg.jqa.down] run return run function rpg:jacques_ally/down_tick
scoreboard players add @s rpg_al_t 1
execute unless items entity @s weapon.offhand minecraft:paper run return run function rpg:jacques_ally/fall
execute if score @s rpg_al_t matches 400.. run return run function rpg:jacques_ally/leave
execute if score @s rpg_al_t matches 360 run tellraw @a[distance=..32] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔊𝔯𝔞𝔫𝔡 𝔐𝔞𝔰𝔱𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"时候到了。愿主与你同在。","color":"#9C9A94","bold":false,"italic":false}]
execute store result score @s rpg_al_hp run data get entity @s Health 1
# 重力（NoAI 的载体自己不会落下）
execute if block ~ ~-0.05 ~ #minecraft:replaceable run tp @s ~ ~-0.5 ~
tag @s add rpg.al.cur
function rpg:jacques_ally/think
tag @s remove rpg.al.cur
particle minecraft:dust_color_transition{from_color:[1.0,0.86,0.45],to_color:[1.0,0.97,0.85],scale:1.2} ~ ~1.2 ~ 0.3 0.6 0.3 0 1
