execute unless score @s rpg_tl_q5 matches 1 run return run tellraw @s ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"孩子","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" ℭ𝔥𝔦𝔩𝔡","color":"#8F7430","italic":false},{"text":"  你是来找我的吗？","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Have you come to find me?","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ch01 voice @s ~ ~ ~ 1 1
tellraw @s ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"孩子","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" ℭ𝔥𝔦𝔩𝔡","color":"#8F7430","italic":false},{"text":"  你是来找我的吗？","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Have you come to find me?","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ch01 voice @s ~ ~ ~ 1 1
tellraw @s ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"孩子","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" ℭ𝔥𝔦𝔩𝔡","color":"#8F7430","italic":false},{"text":"  我迷路了，是那个戴兜帽的叔叔给我饭吃。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"I got lost, and the man in the hood gave me food.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ch02 voice @s ~ ~ ~ 1 1
tellraw @s ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"孩子","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" ℭ𝔥𝔦𝔩𝔡","color":"#8F7430","italic":false},{"text":"  他说别告诉神父，可我觉得他是好人。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"He said not to tell the priest, but I think he's a good man.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ch03 voice @s ~ ~ ~ 1 1
scoreboard players set @s rpg_tl_q5 2
tag @s add rpg.tl.camp
execute as @e[type=minecraft:villager,tag=rpg.tnpc.child,distance=..8,limit=1,sort=nearest] at @s run function rpg:town/life/q/child_gone
tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  孩子说他认得回家的路，先跑回去了。你记下了营地的位置。","color":"#C9A646","bold":false,"italic":false}]
