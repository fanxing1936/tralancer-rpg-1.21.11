function rpg:town/ev/title3
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#B8902F","bold":true,"italic":false},{"text":"审判官","color":"#B8902F","bold":true,"italic":false},{"text":"〗","color":"#B8902F","bold":true,"italic":false},{"text":" ℑ𝔫𝔮𝔲𝔦𝔰𝔦𝔱𝔬𝔯","color":"#8F7430","italic":false},{"text":"  以教廷之名：此女与恶魔立约，明日日出，火刑。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"In the name of the Church: this woman has made a pact with demons. At sunrise, she burns.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.iq01 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#B8902F","bold":true,"italic":false},{"text":"审判官","color":"#B8902F","bold":true,"italic":false},{"text":"〗","color":"#B8902F","bold":true,"italic":false},{"text":" ℑ𝔫𝔮𝔲𝔦𝔰𝔦𝔱𝔬𝔯","color":"#8F7430","italic":false},{"text":"  谁替她求情，谁就和她同罪。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Whoever pleads for her shares her guilt.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.iq02 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
scoreboard players set #ph rpg_te 1
scoreboard players set #tt rpg_te 0
bossbar set rpg:town_ev max 4
bossbar set rpg:town_ev value 1
execute as @e[type=minecraft:marker,tag=rpg.tw.at.plaza] if score @s rpg_tw_id = #run rpg_te at @s run execute facing entity @e[type=minecraft:marker,tag=rpg.tw.in.center,limit=1,sort=nearest] feet rotated ~ 0 run function rpg:town/ev/w/stage
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  刑台上绑着一个人。去刑台后面的巷子，有人在等你。","color":"#9C9A94","bold":false,"italic":false}]
