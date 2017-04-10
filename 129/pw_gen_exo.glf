# Pointwise V17.3R5C4 Journal file - Thu Mar 30 10:46:45 2017

package require PWI_Glyph 2.17.3

pw::Application setUndoMaximumLevels 5
pw::Application reset
pw::Application markUndoLevel {Journal Reset}

pw::Application clearModified

set _TMP(mode_2) [pw::Application begin GridImport]
  $_TMP(mode_2) initialize -type Automatic {/Users/mhenryde/wind/backStep/129/backstep5_2levdn.cgns}
  $_TMP(mode_2) read
  $_TMP(mode_2) convert
$_TMP(mode_2) end
unset _TMP(mode_2)
pw::Application markUndoLevel {Import Grid}

pw::Application setCAESolver {EXODUS II} 3
pw::Application markUndoLevel {Select Solver}

set _DM(1) [pw::GridEntity getByName "dom-3"]
set _TMP(split_params) [list]
lappend _TMP(split_params) [lindex [$_DM(1) closestCoordinate {-110 0 1}] 1]
lappend _TMP(split_params) [lindex [$_DM(1) closestCoordinate {-110 0 1}] 1]
set _TMP(PW_1) [$_DM(1) split -J $_TMP(split_params)]
unset _TMP(split_params)
unset _TMP(PW_1)
pw::Application markUndoLevel {Split}

set _DM(2) [pw::GridEntity getByName "dom-6"]
set _TMP(split_params) [list]
lappend _TMP(split_params) [lindex [$_DM(2) closestCoordinate {-110 0 1}] 1]
set _TMP(PW_2) [$_DM(2) split -J $_TMP(split_params)]
unset _TMP(split_params)
unset _TMP(PW_2)
pw::Application markUndoLevel {Split}

set _DM(3) [pw::GridEntity getByName "dom-6-split-1"]
set _DM(4) [pw::GridEntity getByName "dom-6-split-2"]
set _DM(5) [pw::GridEntity getByName "dom-5"]
set _DM(6) [pw::GridEntity getByName "dom-17"]
set _DM(7) [pw::GridEntity getByName "dom-1"]
set _DM(8) [pw::GridEntity getByName "dom-2"]
set _DM(9) [pw::GridEntity getByName "dom-4"]
set _DM(10) [pw::GridEntity getByName "dom-7"]
set _DM(11) [pw::GridEntity getByName "dom-9"]
set _DM(12) [pw::GridEntity getByName "dom-10"]
set _DM(13) [pw::GridEntity getByName "dom-11"]
set _DM(14) [pw::GridEntity getByName "dom-12"]
set _DM(15) [pw::GridEntity getByName "dom-13"]
set _DM(16) [pw::GridEntity getByName "dom-14"]
set _DM(17) [pw::GridEntity getByName "dom-15"]
set _DM(18) [pw::GridEntity getByName "dom-16"]
set _DM(19) [pw::GridEntity getByName "dom-18"]
set _DM(20) [pw::GridEntity getByName "dom-19"]
set _DM(21) [pw::GridEntity getByName "dom-21"]
set _DM(22) [pw::GridEntity getByName "dom-22"]
set _DM(23) [pw::GridEntity getByName "dom-23"]
set _DM(24) [pw::GridEntity getByName "dom-24"]
set _DM(25) [pw::GridEntity getByName "dom-3-split-1"]
set _DM(26) [pw::GridEntity getByName "dom-3-split-2"]
set _BL(1) [pw::GridEntity getByName "Zone   1"]
set _BL(2) [pw::GridEntity getByName "Zone   2"]
set _BL(3) [pw::GridEntity getByName "Zone   3"]
set _BL(4) [pw::GridEntity getByName "Zone   4"]
set _TMP(PW_3) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_4) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_5) [pw::BoundaryCondition getByName "bc-2"]
unset _TMP(PW_4)
$_TMP(PW_5) setName "back"
pw::Application markUndoLevel {Name BC}

set _TMP(PW_6) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_7) [pw::BoundaryCondition getByName "bc-3"]
unset _TMP(PW_6)
$_TMP(PW_7) setName "front"
pw::Application markUndoLevel {Name BC}

set _TMP(PW_8) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_9) [pw::BoundaryCondition getByName "bc-4"]
unset _TMP(PW_8)
$_TMP(PW_9) setName "inlet"
pw::Application markUndoLevel {Name BC}

set _TMP(PW_10) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_11) [pw::BoundaryCondition getByName "bc-5"]
unset _TMP(PW_10)
$_TMP(PW_11) setName "outflow"
pw::Application markUndoLevel {Name BC}

set _TMP(PW_12) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_13) [pw::BoundaryCondition getByName "bc-6"]
unset _TMP(PW_12)
$_TMP(PW_13) setName "lower"
pw::Application markUndoLevel {Name BC}

$_TMP(PW_13) setName "bottom_sym"
pw::Application markUndoLevel {Name BC}

set _TMP(PW_14) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_15) [pw::BoundaryCondition getByName "bc-7"]
unset _TMP(PW_14)
$_TMP(PW_15) setName "top_sym"
pw::Application markUndoLevel {Name BC}

$_TMP(PW_11) setName "outlet"
pw::Application markUndoLevel {Name BC}

set _TMP(PW_16) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_17) [pw::BoundaryCondition getByName "bc-8"]
unset _TMP(PW_16)
$_TMP(PW_17) setName "bottom_"
pw::Application markUndoLevel {Name BC}

$_TMP(PW_13) setName "bottomsym"
pw::Application markUndoLevel {Name BC}

$_TMP(PW_15) setName "topsym"
pw::Application markUndoLevel {Name BC}

$_TMP(PW_17) setName "bottomwall"
pw::Application markUndoLevel {Name BC}

set _TMP(PW_18) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_19) [pw::BoundaryCondition getByName "bc-9"]
unset _TMP(PW_18)
$_TMP(PW_19) setName "topwall"
pw::Application markUndoLevel {Name BC}

$_TMP(PW_5) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_7) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_9) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_11) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_13) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_15) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_17) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_19) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

unset _TMP(PW_3)
unset _TMP(PW_5)
unset _TMP(PW_7)
unset _TMP(PW_9)
unset _TMP(PW_11)
unset _TMP(PW_13)
unset _TMP(PW_15)
unset _TMP(PW_17)
unset _TMP(PW_19)
set _TMP(PW_20) [pw::BoundaryCondition getByName "Unspecified"]
unset _TMP(PW_20)
set _TMP(PW_21) [pw::BoundaryCondition getByName "back"]
unset _TMP(PW_21)
set _TMP(PW_22) [pw::BoundaryCondition getByName "front"]
unset _TMP(PW_22)
set _TMP(PW_23) [pw::BoundaryCondition getByName "inlet"]
unset _TMP(PW_23)
set _TMP(PW_24) [pw::BoundaryCondition getByName "outlet"]
unset _TMP(PW_24)
set _TMP(PW_25) [pw::BoundaryCondition getByName "bottomsym"]
unset _TMP(PW_25)
set _TMP(PW_26) [pw::BoundaryCondition getByName "topsym"]
unset _TMP(PW_26)
set _TMP(PW_27) [pw::BoundaryCondition getByName "bottomwall"]
unset _TMP(PW_27)
set _TMP(PW_28) [pw::BoundaryCondition getByName "topwall"]
unset _TMP(PW_28)
set _TMP(PW_29) [pw::BoundaryCondition getByName "Unspecified"]
unset _TMP(PW_29)
set _TMP(PW_30) [pw::BoundaryCondition getByName "back"]
unset _TMP(PW_30)
set _TMP(PW_31) [pw::BoundaryCondition getByName "front"]
unset _TMP(PW_31)
set _TMP(PW_32) [pw::BoundaryCondition getByName "inlet"]
unset _TMP(PW_32)
set _TMP(PW_33) [pw::BoundaryCondition getByName "outlet"]
unset _TMP(PW_33)
set _TMP(PW_34) [pw::BoundaryCondition getByName "bottomsym"]
unset _TMP(PW_34)
set _TMP(PW_35) [pw::BoundaryCondition getByName "topsym"]
unset _TMP(PW_35)
set _TMP(PW_36) [pw::BoundaryCondition getByName "bottomwall"]
unset _TMP(PW_36)
set _TMP(PW_37) [pw::BoundaryCondition getByName "topwall"]
unset _TMP(PW_37)
set _TMP(PW_38) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_39) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_40) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_41) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_42) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_43) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_44) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_45) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_46) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_40) apply [list [list $_BL(1) $_DM(9)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_40) apply [list [list $_BL(2) $_DM(12)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_40) apply [list [list $_BL(3) $_DM(18)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_40) apply [list [list $_BL(4) $_DM(22)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_45) apply [list [list $_BL(1) $_DM(26)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_45) apply [list [list $_BL(2) $_DM(11)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_45) apply [list [list $_BL(3) $_DM(17)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_38)
unset _TMP(PW_39)
unset _TMP(PW_40)
unset _TMP(PW_41)
unset _TMP(PW_42)
unset _TMP(PW_43)
unset _TMP(PW_44)
unset _TMP(PW_45)
unset _TMP(PW_46)
set _TMP(PW_47) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_48) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_49) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_50) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_51) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_52) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_53) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_54) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_55) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_54) apply [list [list $_BL(4) $_DM(21)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_47)
unset _TMP(PW_48)
unset _TMP(PW_49)
unset _TMP(PW_50)
unset _TMP(PW_51)
unset _TMP(PW_52)
unset _TMP(PW_53)
unset _TMP(PW_54)
unset _TMP(PW_55)
set _TMP(PW_56) [pw::BoundaryCondition getByName "Unspecified"]
unset _TMP(PW_56)
set _TMP(PW_57) [pw::BoundaryCondition getByName "back"]
unset _TMP(PW_57)
set _TMP(PW_58) [pw::BoundaryCondition getByName "front"]
unset _TMP(PW_58)
set _TMP(PW_59) [pw::BoundaryCondition getByName "inlet"]
unset _TMP(PW_59)
set _TMP(PW_60) [pw::BoundaryCondition getByName "outlet"]
unset _TMP(PW_60)
set _TMP(PW_61) [pw::BoundaryCondition getByName "bottomsym"]
unset _TMP(PW_61)
set _TMP(PW_62) [pw::BoundaryCondition getByName "topsym"]
unset _TMP(PW_62)
set _TMP(PW_63) [pw::BoundaryCondition getByName "bottomwall"]
unset _TMP(PW_63)
set _TMP(PW_64) [pw::BoundaryCondition getByName "topwall"]
unset _TMP(PW_64)
set _CN(1) [pw::GridEntity getByName "con-14"]
set _CN(2) [pw::GridEntity getByName "con-28"]
set _CN(3) [pw::GridEntity getByName "con-13"]
set _TMP(split_params) [list]
lappend _TMP(split_params) [lindex [$_DM(16) closestCoordinate {0 0 1}] 1]
set _TMP(PW_65) [$_DM(16) split -J $_TMP(split_params)]
unset _TMP(split_params)
unset _TMP(PW_65)
pw::Application markUndoLevel {Split}

set _DM(27) [pw::GridEntity getByName "dom-14-split-1"]
set _TMP(PW_66) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_67) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_68) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_69) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_70) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_71) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_72) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_73) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_74) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_73) apply [list [list $_BL(3) $_DM(27)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_74) apply [list [list $_BL(1) $_DM(4)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_74) apply [list [list $_BL(2) $_DM(14)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_74) apply [list [list $_BL(3) $_DM(19)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_74) apply [list [list $_BL(4) $_DM(24)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_69) apply [list [list $_BL(1) $_DM(8)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_66)
unset _TMP(PW_67)
unset _TMP(PW_68)
unset _TMP(PW_69)
unset _TMP(PW_70)
unset _TMP(PW_71)
unset _TMP(PW_72)
unset _TMP(PW_73)
unset _TMP(PW_74)
set _TMP(PW_75) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_76) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_77) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_78) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_79) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_80) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_81) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_82) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_83) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_80) apply [list [list $_BL(1) $_DM(25)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_75)
unset _TMP(PW_76)
unset _TMP(PW_77)
unset _TMP(PW_78)
unset _TMP(PW_79)
unset _TMP(PW_80)
unset _TMP(PW_81)
unset _TMP(PW_82)
unset _TMP(PW_83)
set _TMP(PW_84) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_85) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_86) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_87) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_88) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_89) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_90) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_91) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_92) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_90) apply [list [list $_BL(1) $_DM(3)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_84)
unset _TMP(PW_85)
unset _TMP(PW_86)
unset _TMP(PW_87)
unset _TMP(PW_88)
unset _TMP(PW_89)
unset _TMP(PW_90)
unset _TMP(PW_91)
unset _TMP(PW_92)
set _TMP(PW_93) [pw::BoundaryCondition getByName "Unspecified"]
unset _TMP(PW_93)
set _TMP(PW_94) [pw::BoundaryCondition getByName "back"]
unset _TMP(PW_94)
set _TMP(PW_95) [pw::BoundaryCondition getByName "front"]
unset _TMP(PW_95)
set _TMP(PW_96) [pw::BoundaryCondition getByName "inlet"]
unset _TMP(PW_96)
set _TMP(PW_97) [pw::BoundaryCondition getByName "outlet"]
unset _TMP(PW_97)
set _TMP(PW_98) [pw::BoundaryCondition getByName "bottomsym"]
unset _TMP(PW_98)
set _TMP(PW_99) [pw::BoundaryCondition getByName "topsym"]
unset _TMP(PW_99)
set _TMP(PW_100) [pw::BoundaryCondition getByName "bottomwall"]
unset _TMP(PW_100)
set _TMP(PW_101) [pw::BoundaryCondition getByName "topwall"]
unset _TMP(PW_101)
set _TMP(PW_102) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_103) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_104) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_105) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_106) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_107) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_108) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_109) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_110) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_103) apply [list [list $_BL(1) $_DM(7)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_102)
unset _TMP(PW_103)
unset _TMP(PW_104)
unset _TMP(PW_105)
unset _TMP(PW_106)
unset _TMP(PW_107)
unset _TMP(PW_108)
unset _TMP(PW_109)
unset _TMP(PW_110)
set _TMP(PW_111) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_112) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_113) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_114) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_115) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_116) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_117) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_118) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_119) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_112) apply [list [list $_BL(2) $_DM(10)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_111)
unset _TMP(PW_112)
unset _TMP(PW_113)
unset _TMP(PW_114)
unset _TMP(PW_115)
unset _TMP(PW_116)
unset _TMP(PW_117)
unset _TMP(PW_118)
unset _TMP(PW_119)
set _TMP(PW_120) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_121) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_122) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_123) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_124) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_125) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_126) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_127) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_128) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_121) apply [list [list $_BL(3) $_DM(15)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_120)
unset _TMP(PW_121)
unset _TMP(PW_122)
unset _TMP(PW_123)
unset _TMP(PW_124)
unset _TMP(PW_125)
unset _TMP(PW_126)
unset _TMP(PW_127)
unset _TMP(PW_128)
set _TMP(PW_129) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_130) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_131) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_132) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_133) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_134) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_135) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_136) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_137) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_130) apply [list [list $_BL(4) $_DM(20)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_129) apply [list [list $_BL(4) $_DM(20)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_130) apply [list [list $_BL(4) $_DM(20)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_129)
unset _TMP(PW_130)
unset _TMP(PW_131)
unset _TMP(PW_132)
unset _TMP(PW_133)
unset _TMP(PW_134)
unset _TMP(PW_135)
unset _TMP(PW_136)
unset _TMP(PW_137)
set _TMP(PW_138) [pw::BoundaryCondition getByName "Unspecified"]
set _TMP(PW_139) [pw::BoundaryCondition getByName "back"]
set _TMP(PW_140) [pw::BoundaryCondition getByName "front"]
set _TMP(PW_141) [pw::BoundaryCondition getByName "inlet"]
set _TMP(PW_142) [pw::BoundaryCondition getByName "outlet"]
set _TMP(PW_143) [pw::BoundaryCondition getByName "bottomsym"]
set _TMP(PW_144) [pw::BoundaryCondition getByName "topsym"]
set _TMP(PW_145) [pw::BoundaryCondition getByName "bottomwall"]
set _TMP(PW_146) [pw::BoundaryCondition getByName "topwall"]
$_TMP(PW_142) apply [list [list $_BL(4) $_DM(23)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_143) setId {2}
pw::Application markUndoLevel {Change BC ID}

$_TMP(PW_143) setId {5}
pw::Application markUndoLevel {Change BC ID}

unset _TMP(PW_138)
unset _TMP(PW_139)
unset _TMP(PW_140)
unset _TMP(PW_141)
unset _TMP(PW_142)
unset _TMP(PW_143)
unset _TMP(PW_144)
unset _TMP(PW_145)
unset _TMP(PW_146)
pw::Application save {/Users/mhenryde/wind/backStep/129/backstep5_2levdn.pw}
set _TMP(mode_3) [pw::Application begin CaeExport [pw::Entity sort [list $_BL(1) $_BL(2) $_BL(3) $_BL(4)]]]
  $_TMP(mode_3) initialize -type CAE {/Users/mhenryde/wind/backStep/129/backstep5_2levdn.exo}
  if {![$_TMP(mode_3) verify]} {
    error "Data verification failed."
  }
  $_TMP(mode_3) write
$_TMP(mode_3) end
unset _TMP(mode_3)
