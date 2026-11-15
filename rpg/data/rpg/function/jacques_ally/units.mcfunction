# 「像玩家一样的单位」的标签（每刻最先刷新；add_ally_units.py 把敌方技能里的 @a 改写成按这些标签选）：
#   rpg.unit 全部玩家 + 友军；.ns 去掉旁观；.nc 去掉创造；.f 去掉旁观与创造（能挨打的人）。友军自己一直带着四个。
tag @a remove rpg.unit
tag @a remove rpg.unit.ns
tag @a remove rpg.unit.nc
tag @a remove rpg.unit.f
tag @a add rpg.unit
tag @a[gamemode=!spectator] add rpg.unit.ns
tag @a[gamemode=!creative] add rpg.unit.nc
tag @a[gamemode=!spectator,gamemode=!creative] add rpg.unit.f
