# 召唤友军雅克（as/at 玩家）：在身前 1.5 格落下。
execute unless score @s rpg_al_id matches 1.. run function rpg:jacques_ally/new_id
scoreboard players operation @s rpg_al_cd = #now rpg_al
scoreboard players add @s rpg_al_cd 3600
scoreboard players operation #own rpg_al = @s rpg_al_id
execute rotated ~ 0 positioned ^ ^ ^1.5 run function rpg:jacques_ally/spawn
playsound minecraft:event.raid.horn player @a[distance=..48] ~ ~ ~ 1.2 1.3
tellraw @s ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔊𝔯𝔞𝔫𝔡 𝔐𝔞𝔰𝔱𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣殿骑士团，听候差遣。","color":"#9C9A94","bold":false,"italic":false}]
