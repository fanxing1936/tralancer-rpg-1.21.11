execute unless score #run rpg_te matches 1.. run return 0
execute unless score #kind rpg_te matches 3 run return 0
execute unless score #ph rpg_te matches 1 run return 0
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#D596F2","bold":true,"italic":false},{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},{"text":"〗","color":"#D596F2","bold":true,"italic":false},{"text":" ℌ𝔬𝔬𝔡𝔢𝔡 𝔐𝔞𝔫","color":"#8F7430","italic":false},{"text":"  嘘。别回头，听我说。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Shh. Don't turn around. Listen.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ew01 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#D596F2","bold":true,"italic":false},{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},{"text":"〗","color":"#D596F2","bold":true,"italic":false},{"text":" ℌ𝔬𝔬𝔡𝔢𝔡 𝔐𝔞𝔫","color":"#8F7430","italic":false},{"text":"  明早要烧的那个人没做过他们说的事。我需要人手。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"The one they're burning at dawn didn't do what they say. I need hands.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ew02 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#D596F2","bold":true,"italic":false},{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},{"text":"〗","color":"#D596F2","bold":true,"italic":false},{"text":" ℌ𝔬𝔬𝔡𝔢𝔡 𝔐𝔞𝔫","color":"#8F7430","italic":false},{"text":"  听好：一个人点火引开圣卫，一个人割绳，一个人挡住审判官。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Listen: one lights a fire to draw the guards, one cuts the ropes, one holds the inquisitor.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ew04 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
execute if score #np rpg_te matches 1 run function rpg:town/ev/w/solo
scoreboard players set #ph rpg_te 2
bossbar set rpg:town_ev value 2
execute as @e[tag=rpg.te.g] run data merge entity @s {NoAI:0b}
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#D596F2","bold":true,"italic":false},{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},{"text":"〗","color":"#D596F2","bold":true,"italic":false},{"text":" ℌ𝔬𝔬𝔡𝔢𝔡 𝔐𝔞𝔫","color":"#8F7430","italic":false},{"text":"  圣卫只打晕，别杀。他们也是被派来的。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Knock the guards out; don't kill them. They were sent too.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ew06 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#D596F2","bold":true,"italic":false},{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},{"text":"〗","color":"#D596F2","bold":true,"italic":false},{"text":" ℌ𝔬𝔬𝔡𝔢𝔡 𝔐𝔞𝔫","color":"#8F7430","italic":false},{"text":"  火起来了！现在！","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Fire's lit! Now!","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ew07 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  火起来了。去刑台割断绳子（右键女巫，站在她身边三秒）。圣卫只打晕，别杀。","color":"#9C9A94","bold":false,"italic":false}]
execute as @e[type=minecraft:marker,tag=rpg.tw.at.plaza] if score @s rpg_tw_id = #run rpg_te at @s run execute positioned ~8 ~ ~8 positioned over motion_blocking_no_leaves run setblock ~ ~ ~ minecraft:fire
execute as @e[type=minecraft:marker,tag=rpg.tw.at.plaza] if score @s rpg_tw_id = #run rpg_te at @s run execute as @e[tag=rpg.tg,tag=rpg.te.g,distance=..20,limit=1] run tp @s ~8 ~ ~8
