# 确认（as/at 玩家）
execute if entity @s[tag=rpg.pr] run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"序章还没结束。","color":"#E6DFCF","bold":false,"italic":false}]
execute if entity @s[tag=rpg.ob.hold] run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"先走完开局。","color":"#E6DFCF","bold":false,"italic":false}]
execute if entity @s[tag=rpg.pl.in] run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"先离开失乐园。","color":"#E6DFCF","bold":false,"italic":false}]
execute if score @s rpg_dt matches 1.. run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"你已经在深渊里了。","color":"#E6DFCF","bold":false,"italic":false}]
execute unless score @s rpg_sef matches 7.. run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"走到第 7 阶「慈悲」，深渊才会打开。","color":"#E6DFCF","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.jqb.center,distance=..64] run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"打完眼前这一场再说。","color":"#E6DFCF","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.slb.center,distance=..64] run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"打完眼前这一场再说。","color":"#E6DFCF","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.mkb.center,distance=..64] run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"打完眼前这一场再说。","color":"#E6DFCF","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.usb.center,distance=..64] run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"打完眼前这一场再说。","color":"#E6DFCF","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.lub.center,distance=..64] run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"打完眼前这一场再说。","color":"#E6DFCF","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.pf.center,distance=..64] run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"打完眼前这一场再说。","color":"#E6DFCF","bold":false,"italic":false}]
execute if score @s rpg_dt_cd matches 1.. run return run function rpg:daath_fight/cd_say
scoreboard players set #slot rpg_dt 0
execute if score #slot rpg_dt matches 0 unless score #b1 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 1
execute if score #slot rpg_dt matches 0 unless score #b2 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 2
execute if score #slot rpg_dt matches 0 unless score #b3 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 3
execute if score #slot rpg_dt matches 0 unless score #b4 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 4
execute if score #slot rpg_dt matches 0 unless score #b5 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 5
execute if score #slot rpg_dt matches 0 unless score #b6 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 6
execute if score #slot rpg_dt matches 0 unless score #b7 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 7
execute if score #slot rpg_dt matches 0 unless score #b8 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 8
execute if score #slot rpg_dt matches 0 unless score #b9 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 9
execute if score #slot rpg_dt matches 0 unless score #b10 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 10
execute if score #slot rpg_dt matches 0 unless score #b11 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 11
execute if score #slot rpg_dt matches 0 unless score #b12 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 12
execute if score #slot rpg_dt matches 0 unless score #b13 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 13
execute if score #slot rpg_dt matches 0 unless score #b14 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 14
execute if score #slot rpg_dt matches 0 unless score #b15 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 15
execute if score #slot rpg_dt matches 0 unless score #b16 rpg_dt matches 1 run scoreboard players set #slot rpg_dt 16
execute if score #slot rpg_dt matches 0 run return run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"深渊里已经站满了人，稍后再来。","color":"#E6DFCF","bold":false,"italic":false}]
function rpg:daath_fight/begin
