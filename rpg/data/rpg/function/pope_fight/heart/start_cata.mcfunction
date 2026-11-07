scoreboard players set #sk rpg_pf 12
scoreboard players set #st rpg_pf 0
scoreboard players set #walking rpg_pf 0
function rpg:pope_fight/heart/clip/cross_beam
tellraw @a[distance=..48] ["",{"text":"〖末影之心〗","color":"#A276BE","bold":true,"italic":false},{"text":" ℌ𝔢𝔞𝔯𝔱 𝔬𝔣 𝔈𝔫𝔡𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"十字灾变：","color":"#E6DFCF","bold":false,"italic":false},{"text":"跪下，对着这十字。贴近我，或者跟着光跑。","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set #dir rpg_pf 0
function rpg:pope_fight/heart/weak_on
playsound rpg:heart_of_ender.mortar_explode hostile @a[distance=..48] ~ ~ ~ 1 0.5
