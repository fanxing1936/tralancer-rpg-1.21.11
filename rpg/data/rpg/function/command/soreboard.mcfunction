##武器计分板
scoreboard objectives add damage minecraft.custom:minecraft.damage_dealt
scoreboard objectives add saber minecraft.custom:minecraft.damage_dealt
scoreboard objectives add wukong minecraft.custom:minecraft.damage_dealt
scoreboard objectives add blow minecraft.custom:minecraft.damage_dealt
scoreboard objectives add chainsaw minecraft.custom:minecraft.damage_dealt
scoreboard objectives add sakura minecraft.custom:minecraft.damage_dealt
scoreboard objectives add typhoon minecraft.custom:minecraft.damage_dealt
scoreboard objectives add soul minecraft.custom:minecraft.damage_dealt
scoreboard objectives add power minecraft.custom:minecraft.damage_dealt
scoreboard objectives add montain minecraft.custom:minecraft.damage_dealt
scoreboard objectives add ashes minecraft.custom:minecraft.damage_dealt
scoreboard objectives add blil minecraft.custom:minecraft.damage_dealt
scoreboard objectives add potion minecraft.custom:minecraft.damage_dealt
scoreboard objectives add pen minecraft.custom:minecraft.damage_dealt
scoreboard objectives add deep minecraft.custom:minecraft.damage_dealt
scoreboard objectives add ink minecraft.custom:minecraft.damage_dealt

scoreboard objectives add sun minecraft.custom:minecraft.damage_dealt
scoreboard objectives add ice minecraft.custom:minecraft.damage_dealt
scoreboard objectives add sea minecraft.custom:minecraft.damage_dealt
scoreboard objectives add steel minecraft.custom:minecraft.damage_dealt

scoreboard objectives add axe minecraft.custom:minecraft.damage_dealt


scoreboard objectives add holy minecraft.custom:minecraft.damage_dealt
scoreboard objectives add devil_weapon minecraft.custom:minecraft.damage_dealt


scoreboard objectives add absorption minecraft.custom:minecraft.damage_taken
scoreboard objectives add pen_ minecraft.custom:minecraft.damage_taken

scoreboard objectives add bubble minecraft.custom:minecraft.damage_dealt



scoreboard objectives add health health
scoreboard objectives add boom health


scoreboard objectives add dark dummy

scoreboard objectives add sakura_step dummy
scoreboard objectives add typhoon_step dummy
scoreboard objectives add ashes_step dummy
scoreboard objectives add blil_step dummy
scoreboard objectives add ashes_level dummy
scoreboard objectives add power_step dummy
scoreboard objectives add wukong_step dummy

scoreboard objectives add ice_step dummy
scoreboard objectives add sea_step dummy

##功能计分板
scoreboard objectives add random dummy
scoreboard objectives add level level

scoreboard objectives add night dummy

scoreboard objectives add wind dummy
scoreboard objectives add sweep dummy
scoreboard objectives add flame dummy


scoreboard objectives add green dummy

scoreboard objectives add time_level dummy

scoreboard objectives add player_armor dummy
scoreboard objectives add player_armor_toughness dummy
scoreboard objectives add player_armor_ dummy
scoreboard objectives add player_armor_toughness_ dummy
scoreboard players set 100 player_armor_toughness 100
scoreboard players set 100 player_armor 100

scoreboard objectives add player_attack_damage dummy
scoreboard objectives add player_attack_speed dummy
scoreboard objectives add player_attack_damage_ dummy
scoreboard objectives add player_attack_speed_ dummy
scoreboard players set 100 player_attack_speed 100
scoreboard players set 100 player_attack_damage 100


scoreboard objectives add loot dummy

scoreboard objectives add trial dummy
scoreboard players set 层数 trial 0

scoreboard objectives add task dummy

scoreboard objectives add devil dummy
scoreboard objectives add devil_hurt minecraft.custom:minecraft.damage_taken



scoreboard objectives add player_level dummy
scoreboard objectives add player_level_ dummy
scoreboard players set 64 player_level_ 64
scoreboard players set 32 player_level_ 32
scoreboard players set 16 player_level_ 16
scoreboard players set 8 player_level_ 8
scoreboard players set 4 player_level_ 4
scoreboard players set 2 player_level_ 2
scoreboard players set 1 player_level_ 1

scoreboard objectives add weapon_level dummy
scoreboard objectives add weapon_level_ dummy
scoreboard objectives add weapon_exp_max dummy
scoreboard objectives add weapon_exp_max_ dummy
scoreboard objectives add weapon_exp dummy
scoreboard objectives add weapon_exp_ dummy
scoreboard players set 4 weapon_exp_max_ 4
scoreboard players set 3 weapon_exp_max_ 3


scoreboard objectives add weapon_xilian dummy
scoreboard objectives add weapon_xilian_ dummy

scoreboard objectives add weapon_attack minecraft.custom:minecraft.damage_dealt


scoreboard objectives add entity_health dummy
scoreboard objectives add entity_base_health dummy


scoreboard objectives add damage_timing dummy
scoreboard objectives add damage_action dummy

# 伪爆炸：Boss 与二阶段侍从的稳定归属
scoreboard objectives add rpg_boom_id dummy

##新增装备技能
scoreboard objectives add truth minecraft.custom:minecraft.damage_dealt
scoreboard objectives add rpg_vine_lash dummy

##双生剑
scoreboard objectives add boaz minecraft.custom:minecraft.damage_dealt
scoreboard objectives add rpg_boaz_stack dummy
scoreboard objectives add rpg_luci_sin dummy
scoreboard objectives add rpg_luci_cd dummy
scoreboard objectives add rpg_luci_use dummy
scoreboard objectives add rpg_levi_time dummy
scoreboard objectives add rpg_levi_beat dummy
scoreboard objectives add rpg_levi_hp dummy
scoreboard objectives add rpg_levi_charge dummy
scoreboard objectives add rpg_levi_hold dummy
scoreboard objectives add rpg_rune_roll dummy
scoreboard objectives add rpg_rune_ebb dummy
scoreboard objectives add rpg_tide dummy
scoreboard objectives add rpg_quake dummy
scoreboard objectives add rpg_shade dummy
scoreboard objectives add rpg_forge dummy
scoreboard objectives add rpg_forge_chg dummy
scoreboard objectives add rpg_forge_hold dummy
scoreboard objectives add rpg_saw dummy
scoreboard objectives add rpg_taint dummy
scoreboard objectives add rpg_hud dummy
scoreboard objectives add rpg_hud_p dummy
scoreboard objectives add rpg_hud_t dummy
scoreboard objectives add rpg_taint_t dummy
scoreboard objectives add rpg_vac dummy
scoreboard objectives add rpg_rite dummy
scoreboard objectives add rpg_totem dummy
scoreboard objectives add rpg_holy dummy
scoreboard objectives add rpg_vac_x dummy
scoreboard objectives add rpg_hud_on dummy
scoreboard objectives add rpg_fall dummy
scoreboard objectives add rpg_dm_cd dummy
scoreboard objectives add rpg_dm_lord dummy
scoreboard objectives add rpg_dm_casts dummy
scoreboard objectives add rpg_dm_ult dummy
scoreboard objectives add rpg_dm_last dummy
scoreboard players set #hud_seg rpg_hud 10
scoreboard players set #hud_mini rpg_hud 5
scoreboard players set #hud_full rpg_hud 30
scoreboard players set #taint_max rpg_hud 100
scoreboard players set #fall_max rpg_hud 60
scoreboard players set #inv_full rpg_hud 200
scoreboard players set #holy_full rpg_hud 3600
scoreboard objectives add rpg_pact dummy
scoreboard objectives add rpg_pact_cd dummy
scoreboard objectives add rpg_pact_t dummy
scoreboard objectives add rpg_hud_dm dummy
scoreboard objectives add rpg_hud_dmt dummy
scoreboard players set #pact_full rpg_hud 300
scoreboard players set #two rpg_pact 2
scoreboard objectives add rpg_squad dummy
scoreboard objectives add rpg_sq_mode dummy
scoreboard objectives add rpg_sq_cd dummy
scoreboard objectives add rpg_sq_t dummy
scoreboard objectives add rpg_sq_n dummy
scoreboard objectives add rpg_sq_have dummy
scoreboard objectives add rpg_sq_aim dummy
scoreboard objectives add rpg_sq_stance dummy
scoreboard objectives add rpg_sq_tier dummy
scoreboard objectives add rpg_sq_roll dummy
scoreboard objectives add rpg_sq_fr dummy
scoreboard objectives add rpg_sq_slot dummy
scoreboard objectives add rpg_mam dummy
scoreboard objectives add rpg_mam_c dummy
scoreboard objectives add rpg_mam_win dummy
scoreboard objectives add rpg_mam_dw dummy
scoreboard players set #mam_full rpg_hud 40

# 老武器现代化：状态全部归玩家，不再 reset * 互踩
scoreboard objectives add rpg_leg_cd dummy
scoreboard objectives add rpg_pen_mode dummy
scoreboard objectives add rpg_venom dummy
scoreboard objectives add rpg_night_chg dummy
scoreboard objectives add rpg_night_hold dummy
scoreboard objectives add rpg_ashes_chg dummy
scoreboard objectives add rpg_ashes_hold dummy
scoreboard objectives add rpg_wind_chg dummy
scoreboard objectives add rpg_wind_hold dummy
scoreboard objectives add rpg_throne_chg dummy
scoreboard objectives add rpg_throne_hold dummy
scoreboard objectives add rpg_throne_mark dummy
scoreboard objectives add rpg_throne_owner dummy
scoreboard objectives add rpg_legacy_uid dummy
scoreboard objectives add rpg_blil_cd dummy
# 旧镶嵌的 0..50 蓄力映射到十段 HUD。
scoreboard players set #rune5 rpg_hud_p 5
scoreboard objectives add rpg_hud_m dummy
scoreboard objectives add rpg_hud_mt dummy
scoreboard objectives add rpg_inv dummy
scoreboard objectives add rpg_inv_id dummy
scoreboard objectives add rpg_boss_slot dummy
scoreboard objectives add rpg_boss_fx dummy
scoreboard objectives add rpg_proj_t dummy
scoreboard objectives add rpg_hp_level dummy
scoreboard objectives add rpg_com_clock dummy
scoreboard objectives add rpg_ex_stage dummy
scoreboard objectives add rpg_ex_time dummy
scoreboard objectives add rpg_ex_hp dummy
scoreboard objectives add rpg_ex_tmp dummy
scoreboard objectives add rpg_rite_id dummy
scoreboard objectives add rpg_case1 dummy
scoreboard objectives add rpg_case2 dummy
scoreboard objectives add rpg_case3 dummy
scoreboard objectives add rpg_case4 dummy
scoreboard objectives add rpg_case5 dummy
scoreboard objectives add rpg_case6 dummy
scoreboard objectives add rpg_case7 dummy
scoreboard objectives add rpg_ex_stab dummy
scoreboard objectives add rpg_ex_counter dummy
scoreboard objectives add rpg_ex_kind dummy
scoreboard objectives add rpg_ex_ctime dummy
scoreboard objectives add rpg_ex_ransom dummy
scoreboard objectives add rpg_ex_slots dummy
scoreboard objectives add rpg_ex_toolcd dummy
scoreboard objectives add rpg_ex_choice trigger
scoreboard objectives add rpg_panel trigger
scoreboard objectives add rpg_ex_xp dummy
scoreboard objectives add rpg_ex_lvl dummy
scoreboard objectives add rpg_ex_path dummy
scoreboard objectives add rpg_ex_seen dummy
scoreboard objectives add rpg_ex_prev dummy
scoreboard objectives add rpg_ex_use minecraft.used:minecraft.goat_horn
scoreboard objectives add rpg_seal_t dummy
scoreboard objectives add rpg_seal_roll dummy
scoreboard objectives add rpg_seal_i dummy
scoreboard objectives add rpg_prop_t dummy
scoreboard objectives add rpg_ex_phase dummy
scoreboard objectives add rpg_ex_pressure dummy
scoreboard objectives add rpg_ex_pressure_roll dummy
scoreboard objectives add rpg_ex_wave dummy
scoreboard objectives add rpg_ex_wave_kind dummy
scoreboard objectives add rpg_ex_struggle dummy
scoreboard objectives add rpg_ex_hitcd dummy
scoreboard objectives add rpg_ex_usecd dummy
scoreboard objectives add rpg_ex_hud dummy
scoreboard objectives add rpg_ex_hud_t dummy
scoreboard objectives add rpg_mn_lord dummy
scoreboard objectives add rpg_mn_role dummy
scoreboard objectives add rpg_mn_cd dummy
scoreboard objectives add rpg_mn_tick dummy
scoreboard objectives add rpg_mn_slot dummy
scoreboard objectives add rpg_lt_tick dummy
scoreboard objectives add rpg_lt_fill dummy
scoreboard objectives add rpg_lt_usecd dummy
scoreboard objectives add rpg_lt_covenant dummy
scoreboard objectives add rpg_lt_bless dummy
scoreboard objectives add rpg_lt_divine dummy
scoreboard objectives add rpg_lt_div_cd dummy
scoreboard objectives add rpg_lt_div_max dummy
scoreboard objectives add rpg_lt_div_t dummy
scoreboard objectives add rpg_lt_regen dummy
scoreboard objectives add rpg_lt_auth dummy
scoreboard objectives add rpg_lt_hp dummy
scoreboard objectives add rpg_lt_max dummy
scoreboard objectives add rpg_lt_owner dummy
scoreboard objectives add rpg_lt_gather dummy
scoreboard objectives add rpg_lt_claim dummy
scoreboard objectives add rpg_lt_migrate dummy
scoreboard players set #three rpg_lt_max 3
scoreboard players set #four rpg_lt_max 4
scoreboard players set #five rpg_lt_max 5
scoreboard players set #twenty rpg_lt_max 20
scoreboard players set #hundred rpg_lt_max 100
