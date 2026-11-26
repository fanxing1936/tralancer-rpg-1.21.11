# 收场 10：清实体、放开区块
execute in rpg:daath positioned 5120.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 5088 -32 5152 32
bossbar set rpg:daath_10 players
bossbar set rpg:daath_10 visible false
scoreboard players set #b10 rpg_dt 0
data remove storage rpg:daath s10
