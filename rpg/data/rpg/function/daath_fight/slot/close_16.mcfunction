# 收场 16：清实体、放开区块
execute in rpg:daath positioned 8192.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 8160 -32 8224 32
bossbar set rpg:daath_16 players
bossbar set rpg:daath_16 visible false
scoreboard players set #b16 rpg_dt 0
data remove storage rpg:daath s16
