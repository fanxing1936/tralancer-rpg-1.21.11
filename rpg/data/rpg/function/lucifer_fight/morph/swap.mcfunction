# 换成树：挂上外观只读的 rpg.lu.phase2，当刻直接换装，不等下一刻。
tag @s add rpg.lu.phase2
function rpg:lucifer_fight/grow
function rpg:lucifer_p2/dress
tellraw @a[distance=..32] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"伊甸的树重新长了出来。","color":"#9C9A94","bold":false,"italic":false}]
particle block{block_state:{Name:"minecraft:moss_block"}} ~ ~3 ~ 2.5 3 2.5 0.1 80
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.4} ~ ~3 ~ 2 3 2 0.05 60
particle spore_blossom_air ~ ~4 ~ 3 3 3 0 60
execute positioned ~ ~3.5 ~ run function rpg:lucifer_fight/morph/burst
