scoreboard players set #sk rpg_pf 10
scoreboard players set #st rpg_pf 0
scoreboard players set #walking rpg_pf 0
function rpg:pope_fight/heart/clip/mortar
tellraw @a[distance=..48] ["",{"text":"〖末影之心〗","color":"#A276BE","bold":true,"italic":false},{"text":" ℌ𝔢𝔞𝔯𝔱 𝔬𝔣 𝔈𝔫𝔡𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"千面降临：","color":"#E6DFCF","bold":false,"italic":false},{"text":"这些都是被圣座吃掉的脸。别站到光束里。","color":"#9C9A94","bold":false,"italic":false}]
playsound rpg:heart_of_ender.mortar_explode hostile @a[distance=..48] ~ ~ ~ 1 0.5
particle flash{color:13997810} ~ ~3 ~ 0 0 0 0 1 normal
