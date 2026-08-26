function rpg:campaign/beelzebub/debug/stage_reset
tag @s add rpg.ch1.debug.no_commit
tag @s add rpg.ch1.witness.ready
scoreboard players set @s rpg_ch1_stage 7
function rpg:campaign/beelzebub/stage/7_enter
