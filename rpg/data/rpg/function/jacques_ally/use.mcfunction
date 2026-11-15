# 右键圣殿誓约（as 玩家）。按住会每刻触发一次：只认按下的第一刻。
advancement revoke @s only rpg:jacques_ally/use
execute store result score #now rpg_al run time query gametime
scoreboard players operation #gap rpg_al = #now rpg_al
scoreboard players operation #gap rpg_al -= @s rpg_al_lu
scoreboard players operation @s rpg_al_lu = #now rpg_al
execute if score #gap rpg_al matches ..2 run return 0
execute if score @s rpg_al_cd > #now rpg_al run return run function rpg:jacques_ally/use_wait
function rpg:jacques_ally/summon
