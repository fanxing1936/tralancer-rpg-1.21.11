# 圣器碎裂：碎片向外炸开，光环裂成四段（at 中心）。
kill @e[tag=rpg.pf.halo]
kill @e[tag=rpg.pf.vortex]
execute rotated 0.0 -20 run function rpg:pope_fight/fx/shard_0
execute rotated 45.0 -35 run function rpg:pope_fight/fx/shard_1
execute rotated 90.0 -50 run function rpg:pope_fight/fx/shard_2
execute rotated 135.0 -20 run function rpg:pope_fight/fx/shard_3
execute rotated 180.0 -35 run function rpg:pope_fight/fx/shard_4
execute rotated 225.0 -50 run function rpg:pope_fight/fx/shard_5
execute rotated 270.0 -20 run function rpg:pope_fight/fx/shard_6
execute rotated 315.0 -35 run function rpg:pope_fight/fx/shard_7
execute rotated 45 -10 positioned ~ ~2.4 ~ run function rpg:pope_fight/fx/arc
execute rotated 135 -10 positioned ~ ~2.4 ~ run function rpg:pope_fight/fx/arc
execute rotated 225 -10 positioned ~ ~2.4 ~ run function rpg:pope_fight/fx/arc
execute rotated 315 -10 positioned ~ ~2.4 ~ run function rpg:pope_fight/fx/arc
particle flash{color:16773800} ~ ~1 ~ 0 0 0 0 1 force
