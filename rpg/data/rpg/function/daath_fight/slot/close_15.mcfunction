# 收场 15：清实体、放开区块
execute in rpg:daath positioned 7680.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 7648 -32 7712 32
bossbar set rpg:daath_15 players
bossbar set rpg:daath_15 visible false
scoreboard players set #b15 rpg_dt 0
data remove storage rpg:daath s15
