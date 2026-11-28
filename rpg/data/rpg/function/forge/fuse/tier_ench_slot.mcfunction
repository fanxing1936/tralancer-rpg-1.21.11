# 祭品是重锤或弓弩：同样看附魔（借 #tier 算，再还原）
scoreboard players set #tier rpg_fg 0
$function rpg:forge/fuse/tier_ench_inv {n:$(n)}
scoreboard players operation #ct rpg_fg = #tier rpg_fg
scoreboard players operation #tier rpg_fg = #keep rpg_fg
