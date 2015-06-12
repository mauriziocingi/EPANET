/*-----------------------------------------------------------------------------
 **   hash.c
 **
 **   Implementation of a simple Hash Table for string storage & retrieval
 **
 **   Original version by L. Rossman
 **   Updated by Open Water Analytics group
 **
 **   The hash table data structure (HTable) is defined in "hash.h".
 **   Interface Functions:
 **      ENHashTablecreate() - creates a hash table
 **      ENHashTableinsert() - inserts a string & its index value into a hash table
 **      ENHashTablefind()   - retrieves the index value of a string from a table
 **      ENHashTablefree()   - frees a hash table
 */

#ifndef __APPLE__
#include <malloc.h>
#else
#include <stdlib.h>
#endif
#include <string.h>
#include "hash.h"

/* djb2 hashing function "has excellent distribution and speed on many different sets of keys and table sizes" */
unsigned int _enHash(char *str);
unsigned int _enHash(char *str)
{
  unsigned int hash = 5381;
  unsigned int retHash;
  int c;
  while ((c = *str++)) {
    hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
  }
  retHash = hash % ENHASHTABLEMAXSIZE;
  return retHash;
}

ENHashTable *ENHashTableCreate()
{
  int i;
  ENHashTable *ht = (ENHashTable *) calloc(ENHASHTABLEMAXSIZE, sizeof(ENHashTable));
  if (ht != NULL) {
    for (i=0; i<ENHASHTABLEMAXSIZE; i++) {
      ht[i] = NULL;
    }
  }
  return(ht);
}

int ENHashTableInsert(ENHashTable *ht, char *key, int data)
{
  unsigned int i = _enHash(key);
  ENHashEntry *entry;
  if ( i >= ENHASHTABLEMAXSIZE ) {
    return(0);
  }
  entry = (ENHashEntry *) malloc(sizeof(ENHashEntry));
  if (entry == NULL) {
    return(0);
  }
  entry->key = key;
  entry->data = data;
  entry->next = ht[i];
  ht[i] = entry;
  return(1);
}

int     ENHashTableFind(ENHashTable *ht, char *key)
{
  unsigned int i = _enHash(key);
  ENHashEntry *entry;
  if ( i >= ENHASHTABLEMAXSIZE ) {
    return(NOTFOUND);
  }
  entry = ht[i];
  while (entry != NULL)
  {
    if ( strcmp(entry->key,key) == 0 ) {
      return(entry->data);
    }
    entry = entry->next;
  }
  return(NOTFOUND);
}

char    *ENHashTableFindKey(ENHashTable *ht, char *key)
{
  unsigned int i = _enHash(key);
  ENHashEntry *entry;
  if ( i >= ENHASHTABLEMAXSIZE ) {
    return(NULL);
  }
  entry = ht[i];
  while (entry != NULL)
  {
    if ( strcmp(entry->key,key) == 0 ) {
      return(entry->key);
    }
    entry = entry->next;
  }
  return(NULL);
}

void    ENHashTableFree(ENHashTable *ht)
{
  ENHashEntry *entry, *nextentry;
  int i;
  for (i=0; i<ENHASHTABLEMAXSIZE; i++)
  {
    entry = ht[i];
    while (entry != NULL)
    {
      nextentry = entry->next;
      free(entry);
      entry = nextentry;
    }
  }
  free(ht);
}
