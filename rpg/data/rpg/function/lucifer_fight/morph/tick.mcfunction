scoreboard players add @s rpg_l2_t 1
scoreboard players set @s rpg_dm_ult 0
execute if score @s rpg_dm_cd matches ..29 run scoreboard players set @s rpg_dm_cd 30
# 苔藓与孢子向他收拢，地下有根须翻动。
execute if score @s rpg_l2_t matches ..39 run particle spore_blossom_air ~ ~2 ~ 4 2 4 0 6
execute if score @s rpg_l2_t matches ..39 run particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.2 ~ 3 0.1 3 0.1 6
execute if score @s rpg_l2_t matches 10 run particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.6} ~ ~1.5 ~ 1.5 1.5 1.5 0.05 30
execute if score @s rpg_l2_t matches 20 run playsound minecraft:block.rooted_dirt.break hostile @a[distance=..32] ~ ~ ~ 1.4 0.5
execute if score @s rpg_l2_t matches 30 run particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.4} ~ ~1.5 ~ 1 2 1 0.08 40
execute if score @s rpg_l2_t matches 40 run function rpg:lucifer_fight/morph/swap
execute if score @s rpg_l2_t matches 41 run function rpg:lucifer_fight/morph/land
execute if score @s rpg_l2_t matches 100 run function rpg:lucifer_fight/morph/end
