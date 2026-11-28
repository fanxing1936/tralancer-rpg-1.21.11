# 工作台「熔铸」页（as/at 玩家）
function rpg:forge/fuse/pre
execute store result storage rpg:forge fu.nc int 1 run scoreboard players get #nc rpg_fg
execute store result storage rpg:forge fu.ns int 1 run scoreboard players get #ns rpg_fg
execute store result storage rpg:forge fu.need int 1 run scoreboard players get #need rpg_fg
execute store result storage rpg:forge fu.st int 1 run scoreboard players get #st rpg_fg
data modify storage rpg:forge fu.now set value "主手没有可熔铸的装备"
data modify storage rpg:forge fu.after set value "—"
execute unless data storage rpg:forge fu{cls:""} if score #g rpg_fg matches 0 run data modify storage rpg:forge fu merge value {now:"残次",after:"普通"}
execute unless data storage rpg:forge fu{cls:""} if score #g rpg_fg matches 1 run data modify storage rpg:forge fu merge value {now:"普通",after:"精良"}
execute unless data storage rpg:forge fu{cls:""} if score #g rpg_fg matches 2 run data modify storage rpg:forge fu merge value {now:"精良",after:"完美"}
execute unless data storage rpg:forge fu{cls:""} if score #g rpg_fg matches 3 run data modify storage rpg:forge fu merge value {now:"完美",after:"完美 + 1 颗淬炼星"}
execute if score #g rpg_fg matches 3 if score #st rpg_fg matches 5.. run data modify storage rpg:forge fu.after set value "已经五颗星，不能再熔"
function rpg:forge/fuse/view_m with storage rpg:forge fu
