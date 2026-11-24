kill @e[type=minecraft:marker,tag=rpg.ev.mk]
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..64,limit=1,sort=nearest] at @s run summon minecraft:marker ~ ~ ~ {Tags:["rpg.ev.mk"]}
execute as @e[type=minecraft:villager,tag=rpg.vacant,distance=..64,limit=1,sort=nearest] run effect give @s minecraft:glowing 60 0 true
function rpg:events/e5/begin
tellraw @a ["",{"text":"〖事件・空缺者显现〗","color":"#62D9E8","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔙𝔞𝔠𝔞𝔫𝔱","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"村子里有一个人不对劲。他在发光。","color":"#9C9A94","bold":false,"italic":false},{"text":"　坐标 ","color":"#9C9A94","bold":false,"italic":false},{"nbt":"cur.x","storage":"rpg:events","color":"#E6DFCF"},{"text":", ","color":"#9C9A94","bold":false,"italic":false},{"nbt":"cur.z","storage":"rpg:events","color":"#E6DFCF"}]
playsound minecraft:ambient.cave master @a ~ ~ ~ 1 1.4
execute as @a[distance=..64,scores={rpg_ob=100}] run function rpg:quest/start_6
