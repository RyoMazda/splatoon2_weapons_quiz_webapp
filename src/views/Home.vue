<template>
  <div class="home">
    <ul class='class-weapons-list'>
      <li>
        <img
          src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCXtjxPKZr5Y28sOL6Z9elUNjkUrrSE8BFtcrejD38pWzhftAc&s' alt="weapon-class" class='small-main-img'
          :class="{ chosen: bigWeaponClassName === 'ALL' }"
          @click="filterWeaponClassName('ALL')"
        >
      </li>
      <li
        v-for="weapon in bigWeaponClassess" :key="weapon.id"
        @click="filterWeaponClassName(weapon.bigClassName_en)"
      >
        <img :src="weaponId2ImagePath(weapon.id)" alt="weapon-class" class="small-main-img"
             :class="{ chosen: bigWeaponClassName === weapon.bigClassName_en }"
        >
      </li>
    </ul>
    <ul v-if="middleClassWeaponsOfChosenBigWeaponClass.length >= 2" class="class-weapons-list">
      <li
        v-for="weapon in middleClassWeaponsOfChosenBigWeaponClass" :key="weapon.id"
        @click="filterMiddleWeaponClassName(weapon.middleClassName_en)"
      >
        <img :src="weaponId2ImagePath(weapon.id)" alt="weapon-class" class="small-main-img"
             :class="{ chosen: middleWeaponClassName === weapon.middleClassName_en }"
        >
      </li>
    </ul>
    <div>
      <span>Life:&nbsp;</span>
      <span v-for="i in remainingLife" :key="i">
        &#10084;
      </span>
    </div>
    <div>
      <span>
        sub: {{ numSubCorrect }}
      </span>
      <span>,&nbsp;</span>
      <span>
        special: {{ numSpecialCorrect }}
      </span>
      <span>
        / {{ numTries }} ({{ numWeapons }})
      </span>
    </div>

    <div v-if="isFinished">
      終わりだし
      <div>
        <h2>復習べき</h2>
        <div
          v-for="weapon in missedWeapons" :key="weapon.id"
        >
          <p>{{ weapon.name }} / {{ weapon.name_en }}</p>
          <ul>
            <li><img :src="weaponId2ImagePath(weapon.id)" alt=""></li>
            <li><img :src="subWeaponId2ImagePath(weapon.subWeaponId)" alt=""></li>
            <li><img :src="specialWeaponId2ImagePath(weapon.specialWeaponId)" alt=""></li>
          </ul>
        </div>
      </div>
    </div>
    <div v-else>
      <!--  Question  -->
      <div class="question">
        <img :src="weaponId2ImagePath(weapon.id)" alt="target weapon" class="main-img">
      </div>

      <!--  Answer  -->
      <div v-if="showAnswer" class="showAnswer">
        <p class="weapon-class-name">
          {{ weapon.bigClassName    }}<span v-if="bigWeaponClassNameEqualsMiddleWeaponClassName">({{ weapon.middleClassName    }})</span>/
          {{ weapon.bigClassName_en }}<span v-if="bigWeaponClassNameEqualsMiddleWeaponClassName">({{ weapon.middleClassName_en }})</span>
        </p>
        <p>{{ weapon.name }} / {{ weapon.name_en }}</p>
        <div class="answer-message">
          <p v-if="isCorrect">
            まあまあじゃん
          </p>
          <p v-else>
            違うし
          </p>
        </div>

        <button @click="goToNextQuiz">Next</button>
      </div>

      <div>
        <div>
          <h3>Choose the correct Sub Weapon</h3>
          <ul>
            <li
                v-for="id in subWeaponIds" :key="id"
                @click="setSubWeaponId(id)"
            >
              <img
                  :src="subWeaponId2ImagePath(id)" alt="sub weapon"
                  :class="{
                  chosen: answerForm.subWeaponId === id,
                  answer: weapon.subWeaponId === id && showAnswer
                }"
              >
            </li>
          </ul>
        </div>
        <div>
          <h3>Choose the correct Special Weapon</h3>
          <ul>
            <li
                v-for="id in specialWeaponIds" :key="id"
                @click="setSpecialWeaponId(id)"
            >
              <img
                  :src="specialWeaponId2ImagePath(id)" alt="special weapon"
                  :class="{
                  chosen: answerForm.specialWeaponId === id,
                  answer: weapon.specialWeaponId === id && showAnswer
                }"
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import weapons from '@/weapons';
const weaponClassRepresentatives = weapons.filter((weapon) => {
  return [92, 93, 94, 96, 97, 95, 141].includes(weapon.id);
});
const middleWeaponClassRepresentatives = weapons.filter((weapon) => {
  return [92, 98, 93, 99, 94, 96, 97, 95, 141].includes(weapon.id);
});

function createArray(start: number, end: number): number[] {
  const foo = [];
  for (let i = start; i <= end; i++) {
    foo.push(i);
  }
  return foo;
}

function getThreeDigitInteger(value: number): string {
  if (value < 10) {
    return '00' + value;
  } else if (value < 100) {
    return '0' + value;
  } else {
    return String(value);
  }
}

function shuffle(array: any[]): void {
  for (let i = array.length - 1; i >= 0; i--) {
    const rand = Math.floor( Math.random() * ( i + 1 ) );
    [array[i], array[rand]] = [array[rand], array[i]];
  }
}

function getNextWeapon(weapons2answer: Weapon[]): Weapon | undefined {
  shuffle(weapons2answer);
  return weapons2answer.pop();
}


function getEmptyAnswerForm(): AnswerForm {
  return {
    subWeaponId: null,
    specialWeaponId: null,
  };
}


@Component({})
export default class Home extends Vue {
  public weapons: Weapon[] = weapons.slice();
  public subWeaponIds: number[] = createArray(11, 23);
  public specialWeaponIds: number[] = createArray(8, 12).concat(createArray(14, 23));
  public numWeapons: number = this.weapons.length;
  public numSubCorrect: number = 0;
  public numSpecialCorrect: number = 0;
  public numTries: number = 0;
  public remainingLife: number = 5;
  public weapon: Weapon | undefined = getNextWeapon(this.weapons);
  public answerForm: AnswerForm = getEmptyAnswerForm();
  public missedWeapons: Weapon[] = [];
  public bigWeaponClassess: Weapon[] = weaponClassRepresentatives;
  public middleWeaponClassess: Weapon[] = middleWeaponClassRepresentatives;
  public bigWeaponClassName: string = 'ALL';
  public middleWeaponClassName: string = 'ALL';

  // --------------------
  // Logic
  // --------------------
  public get isCorrect(): boolean {
    return !!(
      this.weapon &&
      this.answerForm.subWeaponId === this.weapon.subWeaponId &&
      this.answerForm.specialWeaponId === this.weapon.specialWeaponId
    );
  }
  public get isSubCorrect(): boolean {
    return !!(
      this.weapon &&
      this.answerForm.subWeaponId === this.weapon.subWeaponId
    );
  }
  public get isSpecialCorrect(): boolean {
    return !!(
      this.weapon &&
      this.answerForm.specialWeaponId === this.weapon.specialWeaponId
    );
  }

  public get showAnswer(): boolean {
    const showAnswer =  !!(this.answerForm.subWeaponId !== null && this.answerForm.specialWeaponId !== null);
    if (showAnswer) {
      window.scrollTo(0, 0);
    }
    return showAnswer;
  }
  public get isFinished(): boolean {
    return (this.remainingLife <= 0 || !this.weapon);
  }

  public get bigWeaponClassNameEqualsMiddleWeaponClassName(): boolean {
    if (this === undefined) { return false; }
    if (this.weapon === undefined) { return false; }
    return this.weapon.bigClassName !== this.weapon.middleClassName;
  }

  public get middleClassWeaponsOfChosenBigWeaponClass(): Weapon[] {
    if (this === undefined) { return []; }
    return middleWeaponClassRepresentatives.filter((representativeWeapon) => {
      return representativeWeapon.bigClassName_en === this.bigWeaponClassName;
    });
  }

  // --------------------
  // Methods
  // --------------------
  public setSubWeaponId(id: number): void {
    if (!this.showAnswer) {
      this.answerForm.subWeaponId = id;
    }
  }
  public setSpecialWeaponId(id: number): void {
    if (!this.showAnswer) {
      this.answerForm.specialWeaponId = id;
    }
  }
  public filterWeaponClassName(name: string): void {
    this.bigWeaponClassName = name;
    this.middleWeaponClassName = 'ALL';
    this.weapons = weapons.filter((weapon) => {
      return name === 'ALL' || weapon.bigClassName_en === name;
    });
    this.numSubCorrect = 0;
    this.numSpecialCorrect = 0;
    this.numTries = 0;
    this.remainingLife = 5;
    this.answerForm = getEmptyAnswerForm();
    this.missedWeapons = [];
    this.numWeapons = this.weapons.length;
    this.weapon = getNextWeapon(this.weapons);
  }
  public filterMiddleWeaponClassName(name: string): void {
    this.middleWeaponClassName = name;
    this.weapons = weapons.filter((weapon) => {
      return name === 'ALL' || weapon.middleClassName_en === name;
    });
    this.numSubCorrect = 0;
    this.numSpecialCorrect = 0;
    this.numTries = 0;
    this.remainingLife = 5;
    this.answerForm = getEmptyAnswerForm();
    this.missedWeapons = [];
    this.numWeapons = this.weapons.length;
    this.weapon = getNextWeapon(this.weapons);
  }

  public weaponId2ImagePath(id: number): string {
    const ThreeDigitId = getThreeDigitInteger(id);
    return 'https://www.ikaclo.jp/common/images/weapons/main/weapon_' + ThreeDigitId + '.png';
  }

  public subWeaponId2ImagePath(id: number): string {
    const ThreeDigitId = getThreeDigitInteger(id);
    return 'https://www.ikaclo.jp/common/images/weapons/sub/sub_' + ThreeDigitId + '.png';
  }

  public specialWeaponId2ImagePath(id: number): string {
    const ThreeDigitId = getThreeDigitInteger(id);
    return 'https://www.ikaclo.jp/common/images/weapons/special/special_' + ThreeDigitId + '.png';
  }

  public goToNextQuiz(): void {
    this.numTries += 1;

    if (this.isSubCorrect) {
      this.numSubCorrect += 1;
    } else {
      this.remainingLife -= 1;
    }
    if (this.isSpecialCorrect) {
      this.numSpecialCorrect += 1;
    } else {
      if (this.remainingLife !== 0) {
        this.remainingLife -= 1;
      }
    }

    if (!this.isCorrect && this.weapon) {
      this.missedWeapons.push(this.weapon);
    }

    this.answerForm = getEmptyAnswerForm();
    this.weapon = getNextWeapon(this.weapons);
  }

}
</script>


<style scoped lang="scss">
h3 {
  margin: 10px 0 0;
}
ul {
  padding: 0;
  margin-top: 10px;
}
li{
  display: inline;
  list-style-type: none;
}
.main-img {
  width: 100px;
}
.small-main-img {
  width: 36px;
}
.question {
  margin: 16px;
}
img {
  width: 44px;
  border: 4px white solid;
}
img.chosen {
  border: 4px blue solid;
}
img.answer {
  border: 4px red solid;
}

.showAnswer {
  font-size: large;
  font-weight: bold;
  padding: 0 0.2rem;
  .weapon-class-name {
    color: #555;
    font-size: x-small;
  }
  p {
    margin: 2px 0;
  }
  .answer-message {
    margin: 6px 0;
  }
}
button {
  font-size: x-large;
  margin-top: 10px;
}
.class-weapons-list {
  margin: 0 auto;
}
</style>
