<script>
import iclrdata from '@/assets/data.json'

export default {
  data() {
    return {
      headers: [
        { title: "Title", value: 'title' },
        { title: "Keywords", value: 'keywords' },
        {
          title: 'Average Ratings',
          align: 'center',
          children: [
            { title: 'Rating', value: 'avgRating', sortable: true },
            { title: 'Confidence', value: 'avgConfidence', sortable: true },
            { title: 'Prez', value: 'avgPresentation', sortable: true },
            { title: 'Contribution', value: 'avgContribution', sortable: true},
            { title: 'Soundness', value: 'avgSoundness', sortable: true}
          ]
        }

      ],
      iclrdata: iclrdata
    }
  },
  mounted () {
    this.iclrdata.forEach(data => {
      try {
        let totalRating = data.reviews.reduce((acc, review) => acc + review.rating, 0);
        data.avgRating = (totalRating / data.reviews.length).toFixed(2);

        // Calculate the average confidence
        let totalConfidence = data.reviews.reduce((acc, review) => acc + review.confidence, 0);
        data.avgConfidence = (totalConfidence / data.reviews.length).toFixed(2);

        // Calculate the average presentation
        let totalPresentation = data.reviews.reduce((acc, review) => acc + review.presentation, 0);
        data.avgPresentation = (totalPresentation / data.reviews.length).toFixed(2);

        // Calculate the average contribution
        let totalContribution = data.reviews.reduce((acc, review) => acc + review.contribution, 0);
        data.avgContribution = (totalContribution / data.reviews.length).toFixed(2);

        // Calculate the average soundness
        let totalSoundness = data.reviews.reduce((acc, review) => acc + review.soundness, 0);
        data.avgSoundness = (totalSoundness / data.reviews.length).toFixed(2);
      } catch(e) {
        console.log(data, e)
      }
    });
  }
}
</script>

<template lang="pug">
v-layout
  v-main
    v-container(fluid)
      h2 ICLR 2024 Explorer
      div.text-caption Last update: 20:00 11th Nov 2023
      v-data-table(
        :headers="headers"
        :items="iclrdata"
        density="compact"
        item-key="id"
        items-per-page="25"
        )
        template(v-slot:item.title="{ item }")
          div
            a(:href="'https://openreview.net'+item.pdf" target="_blank") {{ item.title }}
            div.text-caption {{  item.primary_area }}
        template(v-slot:item.keywords="{ item }")
          template(v-for="keyword in item.keywords")
            v-chip(class="ma-2" color="primary" size="small") {{ keyword }}
</template>
