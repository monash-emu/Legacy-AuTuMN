<template>
  <md-layout md-align="center">
    <md-whiteframe style="margin-top: 4em; padding: 3em">
      <md-layout 
        md-flex="50" 
        md-align="center" 
        md-column>

        <h2 class="md-display-2">
          {{ title }}
        </h2>

        <form @submit.prevent="submit">

          <md-input-container>
            <label>User name</label>
            <md-input
              v-model="name"
              type="text"
              placeholder="User name"/>
          </md-input-container>

          <md-input-container>
            <label>E-mail address</label>
            <md-input
              v-model="email"
              type="text"
              placeholder="E-mail address"/>
          </md-input-container>

          <md-input-container>
            <label>New Password</label>
            <md-input
              v-model="rawPassword"
              type="password"
              placeholder="New Password"/>
          </md-input-container>

          <md-input-container>
            <label>Confirm Password</label>
            <md-input
              v-model="rawPasswordConfirm"
              type="password"
              placeholder="Confirm Password"/>
          </md-input-container>

          <md-button 
            type="submit" 
            class="md-raised md-primary">
            Save
          </md-button>

          <div 
            v-if="error" 
            style="color: red">
            {{ error }}
          </div>

        </form>

      </md-layout>
    </md-whiteframe>
  </md-layout>
</template>

<script>
import auth from '../modules/auth'
import _ from 'lodash'

export default {
  name: 'EditUser',
  data() {
    let result = {}
    _.assign(result, this.$store.state.user)
    _.assign(result, {
      title: 'Edit Your Details',
      rawPassword: '',
      rawPasswordConfirm: '',
      error: ''
    })
    return result
  },
  methods: {
    async submit() {
      this.error = ''

      let payload = {}
      const keys = ['id', 'name', 'email', 'rawPassword', 'rawPasswordConfirm']
      for (let key of keys) {
        if (this.$data[key]) {
          payload[key] = this.$data[key]
        }
      }

      let response = await auth.update(payload)
      if (response.result) {
        this.error = 'User updated'
      } else {
        console.log('> EditUser.submit fail', response)
        this.error = response.error.message
      }
    }
  }
}
</script>
