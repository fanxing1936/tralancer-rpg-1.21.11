# 往下找地面（最多 8 步），在那里点一小团火
scoreboard players remove #d rpg_jq 1
execute if score #d rpg_jq matches 1.. if block ~ ~-0.5 ~ #minecraft:replaceable positioned ~ ~-0.5 ~ run return run function rpg:jacques_boss/fire/drop
function rpg:jacques_boss/fire/patch
