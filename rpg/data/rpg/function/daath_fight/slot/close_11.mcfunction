# 收场 11：清实体、放开区块
execute in rpg:daath positioned 5632.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 5600 -32 5664 32
bossbar set rpg:daath_11 players
bossbar set rpg:daath_11 visible false
scoreboard players set #b11 rpg_dt 0
data remove storage rpg:daath s11
