<template>
  <div>
    <b-container>
        <h1>Load Files</h1>
        <hr><br><br>
        <b-form-file
            v-model="selectedFiles"
            placeholder="Choose files or drop here..."
            drop-placeholder="Drop files here..."
            multiple
        ></b-form-file>
        <hr>
        <h3>Files:</h3>
        <h5 v-for="(file, idx) in selectedFiles" :key="idx">
            {{ file.name }}
        </h5>
        <br><br>
        <b-button v-if="spinner" variant="primary" @click="upLoadAll">Enviar</b-button>
        <div v-else>
            <b-button variant="primary" disabled>
                <b-spinner small type="grow"></b-spinner>
                Loading...
            </b-button>
            <hr>
            <h1>
            <strong>Creating Inverted Index...</strong>
            <b-spinner class="ml-auto"></b-spinner>
            </h1>
        </div>
        
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Tweets',
  data() {
    return {
      msg: [],
      selectedFiles:[],
      text: '',
      spinner: true,
    };
  },
  methods: {
    async upLoadAll(){
        const fd=new FormData();
        //fd.append('files',this.selectedFiles.length,this.selectedFiles.length)
        for(let i=0; i<this.selectedFiles.length; i++){
            fd.append('json'+i,this.selectedFiles[i],this.selectedFiles[i].name)
        }
        this.spinner = false
        var url='http://127.0.0.1:5000/upload';
        await axios.post(url,fd)
        .then(function(res){
            if(res.status==201)
                console.log("exitos")
                alert("Inverted Index creado!")
            })
        .catch(function(err){
            console.log(err)
        })
        .then(function(){
            console.log("Finish")
        })
        this.spinner = true
    }
  },
  computed: {
        nameSelectedFile(){
            var i;
            let selectFiles = []
            for(i=0;i<this.selectedFiles.length;i++){
                console.log(this.selectedFiles[i].name)
                selectFiles.push(this.selectedFiles[i]);
            }
            return selectFiles
        }
   },
};
</script>