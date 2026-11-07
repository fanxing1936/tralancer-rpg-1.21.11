# 领主倒下：@s 是到达裁决的领主本人，或他留下的死亡探针。
execute unless score @s rpg_dm_lord matches 1..7 run return 0
scoreboard players operation #lord rpg_pact = @s rpg_dm_lord
scoreboard players set #fell rpg_pact 0
execute if score @s rpg_pact_bid matches 1.. run scoreboard players operation #fell rpg_pact = @s rpg_pact_bid
execute as @a[distance=..32,gamemode=!spectator] run function rpg:pact/clear/witness
