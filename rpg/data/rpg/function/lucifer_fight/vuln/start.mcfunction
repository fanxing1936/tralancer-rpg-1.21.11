scoreboard players set @s rpg_l2_st 4
scoreboard players set @s rpg_l2_t 0
attribute @s minecraft:armor modifier remove rpg:lu2f_open
attribute @s minecraft:armor modifier add rpg:lu2f_open -1 add_multiplied_total
function rpg:lucifer_p2/play/jungleabomination_vulnerablefall
tellraw @a[distance=..32] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"根须落空，花心张开了。","color":"#9C9A94","bold":false,"italic":false}]
execute positioned ~ ~5 ~ run function rpg:lucifer_fight/vuln/pollen
