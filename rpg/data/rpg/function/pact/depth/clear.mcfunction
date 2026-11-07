# 契约断了：退回柱印，清掉深契的全部状态。
function rpg:pact/seal/eject_all
function rpg:pact/depth/avatar_off
scoreboard players set @s rpg_pact_lv 0
scoreboard players set @s rpg_pact_dom 0
scoreboard players set @s rpg_pact_bond 0
scoreboard players set @s rpg_pact_cd2 0
scoreboard players set @s rpg_pact_cd3 0
scoreboard players set @s rpg_pact_av 0
scoreboard players set @s rpg_pact_fx 0
