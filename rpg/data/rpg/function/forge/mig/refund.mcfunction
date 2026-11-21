# 迁移时剥下来的旧符文符石，换成新的退回背包。
execute unless data storage rpg:forge mig.refund[0] run return 0
data modify storage rpg:forge g.k set from storage rpg:forge mig.refund[0].k
function rpg:forge/give/one
data remove storage rpg:forge mig.refund[0]
function rpg:forge/mig/refund
