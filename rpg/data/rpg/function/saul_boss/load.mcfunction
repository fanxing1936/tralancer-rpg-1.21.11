scoreboard objectives add rpg_sl dummy
scoreboard objectives add rpg_sl_h dummy
scoreboard objectives add rpg_sl_c dummy
scoreboard objectives add rpg_sl_b dummy
scoreboard objectives add rpg_sl_n dummy
scoreboard objectives add rpg_sl_k dummy
scoreboard objectives add rpg_sl_cb dummy
scoreboard objectives add rpg_sl_busy dummy
scoreboard objectives add rpg_sl_sk dummy
scoreboard objectives add rpg_sl_t dummy
scoreboard objectives add rpg_sl_life dummy
scoreboard objectives add rpg_sl_kd dummy
scoreboard objectives add rpg_sl_i dummy
scoreboard objectives add rpg_sl_s dummy
scoreboard objectives add rpg_sl_dd minecraft.custom:minecraft.damage_dealt
scoreboard objectives add rpg_sl_dd0 dummy
scoreboard objectives add rpg_sl_v dummy
scoreboard objectives add rpg_sl_ur dummy
bossbar add rpg:saul_boss "扫罗"
# 粉色档的原版贴图已由教皇战改成全透明：只显示名字里的位图横幅。
bossbar set rpg:saul_boss color pink
bossbar set rpg:saul_boss style notched_20
bossbar set rpg:saul_boss visible false
function rpg:saul_boss/load2
