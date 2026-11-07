scoreboard players set #sk rpg_pf 11
scoreboard players set #st rpg_pf 0
scoreboard players set #walking rpg_pf 0
function rpg:pope_fight/heart/clip/mortar
tellraw @a[distance=..48] ["",{"text":"〖末影之心〗","color":"#A276BE","bold":true,"italic":false},{"text":" ℌ𝔢𝔞𝔯𝔱 𝔬𝔣 𝔈𝔫𝔡𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"虚空坍缩：","color":"#E6DFCF","bold":false,"italic":false},{"text":"圣器的底，是空的。跑出那个圈。","color":"#9C9A94","bold":false,"italic":false}]
execute positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/collapse
playsound rpg:heart_of_ender.mortar_explode hostile @a[distance=..48] ~ ~ ~ 1 0.5
