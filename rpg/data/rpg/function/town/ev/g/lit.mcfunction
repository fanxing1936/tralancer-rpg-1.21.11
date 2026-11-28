tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  法阵亮了。守住它，别让蝇群扑灭圣火！","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"The circle is lit. Hold it; don't let the swarm smother the fire!","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr15 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
scoreboard players set #ph rpg_te 3
scoreboard players set #tt rpg_te 0
scoreboard players set #stab rpg_te 100
bossbar set rpg:town_ev max 100
bossbar set rpg:town_ev value 100
bossbar set rpg:town_ev name ["",{"text":"别西卜降临","color":"#B5D957","bold":true,"italic":false},{"text":"　法阵稳定度","color":"#9C9A94","bold":false,"italic":false}]
particle minecraft:end_rod ~ ~0.3 ~ 2 0.1 2 0.02 60
playsound minecraft:block.beacon.activate block @a[distance=..32] ~ ~ ~ 1 0.8
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  法阵亮了。守住它两分钟：别让蝇群扑到圣火上（站在法阵里能稳住它）。","color":"#9C9A94","bold":false,"italic":false}]
execute as @e[type=minecraft:marker,tag=rpg.tw.in.granary] if score @s rpg_tw_id = #run rpg_te at @s run function rpg:town/ev/g/avatar
